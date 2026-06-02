# Define all necessary API routes, utilities, and logic for app to run

# Import necessary components and utilities 
from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from config import app, db, api
from models import User, Note, UserSchema, NoteSchema


# Create a class for users to signup
class Signup(Resource):

    # Create a function initially set the data to JSON to create users
    def post(self):
        data = request.get_json()

        # Control flow to create a user
        try:
            user = User(username=data.get('username'))

            # Using the hash setter make sure to encrypt the password
            user.password_hash = data.get('password')

            # Save the new user to the session and commit to db
            db.session.add(user)
            db.session.commit()

            # Store user id to session
            session['user_id'] = user.id
            return UserSchema().dump(user), 201
        
        # Error handling if the user already exists
        except IntegrityError:
            db.session.rollback()
            return {'errors': ['Username already taken']}, 422
        
        # Error handling for any other errors
        except ValueError as e:
            db.session.rollback()
            return {'errors': [str(e)]}, 422


# Create a class for the frontend to check if users are currently logged in during this session
class CheckSession(Resource):

    # Create a function to prove user loggin state
    def get(self):
        user_id = session.get('user_id')

        # Perform error handling
        if user_id:
            user = User.query.filter(User.id == user_id).first()
            return UserSchema().dump(user), 200

        return {'errors': ['Unauthorized']}, 401


# Create a class to authenticate users and stores their id per session
class Login(Resource):

    # Create a function and initially set the data to JSON to authenticate users
    def post(self):

        data = request.get_json()

        # Search username in db
        user = User.query.filter(User.username == data.get('username')).first()

        # Control flow to authenticate users
        if user and user.authenticate(data.get('password')):
            session['user_id'] = user.id
            return UserSchema().dump(user), 200

        # Return message for error handling if no username found that matches
        return {'errors': ['Invalid username or password']}, 401


# Create a class to logout user
class Logout(Resource):

    # Create a function to verifiy if users are even logged in set the session to none 
    def delete(self):
        if not session.get('user_id'):
            return {'errors': ['Unauthorized']}, 401

        session['user_id'] = None
        return {}, 204


# Createa a class to handle all GET and POST for the notes
class NoteList(Resource):

    # Create a function for initially controlling for unauthorized access and set up pagnation
    def get(self):
        if not session.get('user_id'):
            return {'errors': ['Unauthorized']}, 401

        # Set page number via URL
        page = request.args.get('page', 1, type=int)

        # Seach for notes from the logged in user limit to 10
        notes = Note.query.filter(Note.user_id == session['user_id'])\
            .paginate(page=page, per_page=10, error_out=False)

        return {
            'notes': NoteSchema(many=True).dump(notes.items),
            'total': notes.total,        
            'pages': notes.pages,        
            'current_page': notes.page
        }, 200
    
    # Create a function for initially controlling for unauthorized access and create new notes
    def post(self):
        if not session.get('user_id'):
            return {'errors': ['Unauthorized']}, 401

        data = request.get_json()

        # Control flow for creating a new note for the logged in user
        try:
            note = Note(
                title=data.get('title'),
                content=data.get('content'),
                user_id=session['user_id']
            )
            db.session.add(note)
            db.session.commit()
            return NoteSchema().dump(note), 201
        
        # Error handling for failure
        except ValueError as e:
            db.session.rollback()
            return {'errors': [str(e)]}, 422


# Create a class to handle all GET, PATCH, DELETE requests for notes
class NoteDetail(Resource):

    # Create a function for initially controlling for unauthorized access and search for notes
    def get(self, id):
        if not session.get('user_id'):
            return {'errors': ['Unauthorized']}, 401

        # Search notes by id
        note = Note.query.filter(Note.id == id).first()

        # Perform error handling if no note is found by the ID
        if not note:
            return {'errors': ['Note not found']}, 404

        # Prevent users from accessing other users notes
        if note.user_id != session['user_id']:
            return {'errors': ['Unauthorized']}, 401

        return NoteSchema().dump(note), 200
    
    # Create a function for initially controlling for unauthorized access and patching a specific note
    def patch(self, id):
        if not session.get('user_id'):
            return {'errors': ['Unauthorized']}, 401
        
        # Get the first note that matches search criteria
        note = Note.query.filter(Note.id == id).first()

        # Perform error handling if no note found
        if not note:
            return {'errors': ['Note not found']}, 404

        # Prevent users from accessing other users notes
        if note.user_id != session['user_id']:
            return {'errors': ['Unauthorized']}, 401

        data = request.get_json()

        # Control flow to only update whats requested
        try:
            if 'title' in data:
                note.title = data['title']
            if 'content' in data:
                note.content = data['content']

            db.session.commit()
            return NoteSchema().dump(note), 200
        
        # Error handling
        except ValueError as e:
            db.session.rollback()
            return {'errors': [str(e)]}, 422

    # Create a function for initially controlling for unauthorized access and deleting a specific note
    def delete(self, id):
        if not session.get('user_id'):
            return {'errors': ['Unauthorized']}, 401
        
        # Get the first note that matches search criteria
        note = Note.query.filter(Note.id == id).first()

        # Control flow if no note found
        if not note:
            return {'errors': ['Note not found']}, 404

        # Prevent users from accessing other users notes
        if note.user_id != session['user_id']:
            return {'errors': ['Unauthorized']}, 401

        db.session.delete(note)
        db.session.commit()
        return {}, 204


# Register each Resource class to its respective URL route
api.add_resource(Signup, '/signup')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(NoteList, '/notes')
api.add_resource(NoteDetail, '/notes/<int:id>')


if __name__ == '__main__':
    # Run the app on port 5555 with debug mode on
    app.run(port=5555, debug=True)