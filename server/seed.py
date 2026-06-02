# Create seed file for the providing data for the app to initially to run

# Import utilities and modules to run the file and app
from faker import Faker
from config import app, db
from models import User, Note

# Initialize Faker to get fake data 
fake = Faker() 

# Needed for accessing the db seperate from the request
with app.app_context():    
    
    # 1. DELETE RECORDS: display message to the user
    print("--- Deleting Records ---")
    
    # Delete all notes 
    Note.query.delete() 
    
    # Delete all users 
    User.query.delete() 

    # 2. CREATE USERS: display message to the user
    print("--- Creating Users ---")

    # Create a list to store user list
    users = []

    # Create sample fake users
    for fake_user in range(5):

        # Create a random username for fake users
        user = User(username = fake.user_name())

        # Create a password for all fake users
        user.password_hash = "password123"

        # Add this to the session db and append user 
        db.session.add(user)
        users.append(user)

    # Make sure to commit because notes needs users to be populated before doing its part
    db.commit

    # 3. CREATE NOTES: display message to the user
    print("--- Creating Notes ---")

    # Populate fake notes for fake users
    for fake_user in users:
        for fake_notes in range(3):
            note = Note(
                # Create a random 4 word title 
                title = fake.sentence(nb_words = 4)
                
                # Create random content
                content = fake.paragraph(nb_sentences = 3)

                # Link the notes to the fake users 
                user_id = user.id 
            )

        # Add this to the session db 
        db.session.add(note)

    # Make sure to commit notes to db and display message to the user
    db.session.commit()
    print("Done seeding!")



