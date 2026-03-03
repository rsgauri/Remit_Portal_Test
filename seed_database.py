"""
Database Seed Script
Run this to populate the database with sample clients and sources
"""

from app import app, db
from models import Client, Source

with app.app_context():
    # Check if data already exists
    if Client.query.count() > 0:
        print("⚠️  Database already has data. Skipping seed.")
        print(f"   Clients: {Client.query.count()}")
        print(f"   Sources: {Source.query.count()}")
        exit()
    
    print("🌱 Seeding database with sample data...")
    
    # Add sample clients
    clients = [
        Client(name="ABC Corp", city="Mumbai", country="India", contact="9876543210", active="Yes"),
        Client(name="XYZ Ltd", city="Delhi", country="India", contact="9999999999", active="Yes"),
    ]
    
    for client in clients:
        db.session.add(client)
    
    db.session.commit()
    print(f"✅ Added {len(clients)} clients")
    
    # Add sample sources
    sources = [
        Source(client_id=1, name="Email", type="Mail", active="Yes"),
        Source(client_id=2, name="SFTP", type="File", active="Yes"),
    ]
    
    for source in sources:
        db.session.add(source)
    
    db.session.commit()
    print(f"✅ Added {len(sources)} sources")
    
    print("\n✨ Database seeded successfully!")
    print(f"   Total Clients: {Client.query.count()}")
    print(f"   Total Sources: {Source.query.count()}")