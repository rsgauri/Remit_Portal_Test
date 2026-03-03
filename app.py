

from flask import Flask, render_template, request, redirect, send_from_directory
from models import db, RemittanceAdvice, Client, Source
import os
import uuid
import requests
from pdf_extractor import extract_text_from_pdf
import json
import re
from datetime import date

app = Flask(__name__)

# ---------------- CONFIG ----------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///remittance.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = "secret"

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
db.init_app(app)

with app.app_context():
    db.create_all()

# =====================================================
#        UNIVERSAL PDF EXTRACTION ENGINE (NEW)
# =====================================================

def normalize_text(text):
    return re.sub(r'\s+', ' ', text)


def extract_currency_candidates(text):
    """
    Extract all currency amounts (₹ $ € £ INR USD EUR GBP AED etc.)
    """
    currency_pattern = r'''
        (₹|Rs\.?|INR|\$|USD|EUR|€|GBP|£|AED|AUD|CAD)?  
        \s*
        (
            \d{1,3}(?:,\d{2,3})*(?:\.\d{1,2})?
            |
            \d+(?:\.\d{1,2})?
        )
    '''

    matches = re.finditer(currency_pattern, text, re.VERBOSE | re.IGNORECASE)
    amounts = []

    for match in matches:
        currency = match.group(1) or ""
        number = match.group(2)

        clean_number = number.replace(",", "")

        try:
            value = float(clean_number)
            if value > 100:  # avoid invoice numbers
                amounts.append({
                    "raw": match.group(0).strip(),
                    "value": value
                })
        except:
            pass

    return amounts


def extract_total_amount(text):
    """
    1. Try keyword-based match
    2. Else pick largest currency value
    """

    text = normalize_text(text)

    keywords = [
        "Total Amount",
        "Grand Total",
        "Net Payable",
        "Amount Due",
        "Invoice Total",
        "Total"
    ]

    # Try keyword-based extraction
    for keyword in keywords:
        pattern = rf'{keyword}[^0-9₹$€£]*([₹Rs\.INR$USD€EURGBP£AED]*\s*\d{{1,3}}(?:,\d{{2,3}})*(?:\.\d{{1,2}})?)'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    # Fallback → largest value
    candidates = extract_currency_candidates(text)

    if candidates:
        candidates.sort(key=lambda x: x["value"], reverse=True)
        return candidates[0]["raw"]

    return "Not Found"


def extract_with_regex(text):
    """
    Universal extraction logic
    """

    text = normalize_text(text)

    data = {
        "Invoice Number": "Not Found",
        "Invoice Date": "Not Found",
        "Total Amount": "Not Found"
    }

    # ---------------- INVOICE NUMBER ----------------
    invoice_patterns = [
        r'Invoice\s+(?:No\.?|Number|#)\s*:?\s*([A-Z0-9-]+)',
        r'\bINV[- ]?[A-Z0-9-]+'
    ]

    for pattern in invoice_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            inv = match.group(0)
            data["Invoice Number"] = inv.upper().replace(" ", "-")
            break

    # ---------------- INVOICE DATE ----------------
    date_patterns = [
        r'\d{1,2}[-/]\d{1,2}[-/]\d{4}',
        r'\d{1,2}\s+[A-Za-z]{3,}\s+\d{4}',
        r'\d{1,2}-[A-Za-z]{3,}-\d{4}'
    ]

    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            data["Invoice Date"] = match.group(0)
            break

    # ---------------- TOTAL AMOUNT ----------------
    data["Total Amount"] = extract_total_amount(text)

    return data


# ---------------- SMART EXTRACTION ----------------
def smart_extract(text):
    return extract_with_regex(text)


# =====================================================
#                    ROUTES
# =====================================================

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect("/dashboard")
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    remittances = RemittanceAdvice.query.order_by(RemittanceAdvice.id.desc()).all()

    today = date.today()
    today_count = sum(1 for r in remittances if r.created_at.date() == today)

    client_count = Client.query.count()
    source_count = Source.query.count()

    return render_template("dashboard.html",
                           remittances=remittances,
                           today_count=today_count,
                           client_count=client_count,
                           source_count=source_count)


@app.route("/clients")
def clients():
    clients = Client.query.order_by(Client.id).all()
    return render_template("clients.html", clients=clients)


@app.route("/add_client", methods=["GET", "POST"])
def add_client():
    if request.method == "POST":
        client = Client(
            name=request.form['name'],
            city=request.form['city'],
            country=request.form['country'],
            contact=request.form['contact'],
            active=request.form['active']
        )
        db.session.add(client)
        db.session.commit()
        return redirect("/clients")
    return render_template("add_client.html")


@app.route("/sources")
def sources():
    sources = Source.query.order_by(Source.id).all()
    return render_template("sources.html", sources=sources)


@app.route("/add_source", methods=["GET", "POST"])
def add_source():
    if request.method == "POST":
        source = Source(
            client_id=request.form['client_id'],
            name=request.form['name'],
            type=request.form['type'],
            active=request.form['active']
        )
        db.session.add(source)
        db.session.commit()
        return redirect("/sources")

    clients = Client.query.all()
    return render_template("add_source.html", clients=clients)


@app.route("/remittance")
def remittance():
    remittances = RemittanceAdvice.query.order_by(RemittanceAdvice.id.desc()).all()
    return render_template("remittance.html", remittances=remittances)


# ---------------- UPLOAD ----------------
@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        file = request.files["file"]

        if file.filename == "":
            return "No file selected"

        unique_name = str(uuid.uuid4()) + "_" + file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
        file.save(file_path)

        pdf_text = extract_text_from_pdf(file_path)

        data = smart_extract(pdf_text)

        remittance = RemittanceAdvice(
            client_id=1,
            invoice_no=data.get("Invoice Number"),
            invoice_date=data.get("Invoice Date"),
            invoice_amount=data.get("Total Amount"),
            file_path=unique_name
        )

        db.session.add(remittance)
        db.session.commit()

        return redirect("/dashboard")

    return render_template("upload.html")


@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
