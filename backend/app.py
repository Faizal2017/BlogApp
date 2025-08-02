from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")
jwt = JWTManager(app)

client = MongoClient(os.getenv("MONGO_URI"))
db = client.get_database()

app.db = db

from controllers.auth_controller import auth_bp
from controllers.blog_controller import blog_bp

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(blog_bp, url_prefix="/api/blogs")

if __name__ == "__main__":
    app.run(debug=True)
