from app import app, db  # Import your Flask app and db object

# Set up the app context
with app.app_context():
    db.create_all()  # Create the tables in the database
    print("Database tables created successfully.")
