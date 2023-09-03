from flask import Flask

from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.secret_key = "Patato"

AUTHORIZED_USER_IDS = [10,11,12]