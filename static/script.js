// Dummy Clients
const clients = [
    {id: 1, name: "ABC Corp", city: "Mumbai", country: "India", contact: "9876543210", active: "Yes"},
    {id: 2, name: "XYZ Ltd", city: "Delhi", country: "India", contact: "9999999999", active: "Yes"}
];

const clientTable = document.getElementById("clientTable");
if (clientTable) {
    clients.forEach(c => {
        clientTable.innerHTML += `
            <tr>
                <td>${c.id}</td>
                <td>${c.name}</td>
                <td>${c.city}</td>
                <td>${c.country}</td>
                <td>${c.contact}</td>
                <td>${c.active}</td>
            </tr>
        `;
    });
}

// Dummy Sources
const sources = [
    {id: 1, client: 1, name: "Email", type: "Mail", active: "Yes"},
    {id: 2, client: 2, name: "SFTP", type: "File", active: "Yes"}
];

const sourceTable = document.getElementById("sourceTable");
if (sourceTable) {
    sources.forEach(s => {
        sourceTable.innerHTML += `
            <tr>
                <td>${s.id}</td>
                <td>${s.client}</td>
                <td>${s.name}</td>
                <td>${s.type}</td>
                <td>${s.active}</td>
            </tr>
        `;
    });
}

// Dummy Remittance
const remittances = [
    {id: 101, client: 1, source: 1, amount: 5000, currency: "USD", status: "Processed"},
    {id: 102, client: 2, source: 2, amount: 10000, currency: "INR", status: "Pending"}
];

const remittanceTable = document.getElementById("remittanceTable");
if (remittanceTable) {
    remittances.forEach(r => {
        remittanceTable.innerHTML += `
            <tr>
                <td>${r.id}</td>
                <td>${r.client}</td>
                <td>${r.source}</td>
                <td>${r.amount}</td>
                <td>${r.currency}</td>
                <td>${r.status}</td>
            </tr>
        `;
    });
}