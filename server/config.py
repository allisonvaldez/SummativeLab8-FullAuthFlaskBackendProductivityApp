# Set up and configure all Flask extensions and modules to be used globally in the app
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# Initialize Flask app
app = Flask(__name__)

# Create secret key to encrypt and sign session cookies
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'

# Configure the db 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# Do not track modifications 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Trim space from JSON responses 
app.json.compact = False

# Create naming convention for foreign keys contraints for migrations 
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Create a seperate db for metadata configurations   
db = SQLAlchemy(metadata=metadata)

# Ensure migration commands work
migrate = Migrate(app, db)

# Connect db to Flask app  
db.init_app(app)

# Instantiate bcrypt  
bcrypt = Bcrypt(app)

# Instantiate Flask-RESTful API 
api = Api(app)
