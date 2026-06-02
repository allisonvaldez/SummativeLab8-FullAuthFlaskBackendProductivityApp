# Needed for db tables and Python rules

# Import all necessary utilities and components  
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import Schema, fields
from config import db, bcrypt

# Create the User Model (each row is a registered account)
class User(db.Model):
    __tablename__ = "users"

    # Create a primary key with unique id for each user
    id = db.Column(db.Integer, primary_key = True)

    # Create unique usernames for each use
    username = db.Column(db.String, unique=True, nullable=False)

    # Create a column to store the hashed passwords
    _password_hash = db.Column(db.String)

    # Make sure when a user is deleted all of their notes are deleted too
    notes = db.relationship('Note', backref='user', cascade='all, delete-orphan')

    # Create a hybrid_property decorator for the password column and a function to an raise error for trying to read the hash directly
    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password hash is not readable')

    # Create a setter decorator to trigger when the function is called to hash passwords
    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # Createa a function to compare plain text passwords against the hashed
    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

    # Create a validates decorator and a function to validate usernames
    @validates('username')
    def validate_username(self, key, username):

        # Perform error handling for no username provided
        if not username:
            raise ValueError('Username is required')
        return username

    def __repr__(self):
        return f'User {self.username}'


# Create the Note model (each row is a note by a user)
class Note(db.Model):
    __tablename__ = "notes"

    # Create a primary key that has a unique integer for each note
    id = db.Column(db.Integer, primary_key=True)

    # Create a title for the note
    title = db.Column(db.String, nullable=False)

    # Create content for the note
    content = db.Column(db.String, nullable=False)

    # Create note creation demographics
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Create the foreign key to link the note to the creator
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Create validates decorator to make sure each note has a title and a function to ensure it
    @validates('title')
    def validate_title(self, key, title):
        
        # Perform error handling
        if not title:
            raise ValueError('Title is required')
        return title

    # Create a validates decorator to ensure each not has content and a function to ensure it
    @validates('content')
    def validate_content(self, key, content):
        
        # Perform error handling
        if not content:
            raise ValueError('Content is required')
        return content

    def __repr__(self):
        return f'Note {self.title}'


# Create Marshmallow schema to format JSON responses for users
class UserSchema(Schema):
    id = fields.Int()       
    username = fields.String()

# Create Marshmallow schema to format JSON responses for notes
class NoteSchema(Schema):
    id = fields.Int()              
    title = fields.String()       
    content = fields.String()      
    created_at = fields.DateTime() 
    user_id = fields.Int()         
    user = fields.Nested(UserSchema())