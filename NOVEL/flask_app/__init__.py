from flask import Flask


app = Flask(__name__)

app.secret_key = "Patato"

AUTHORIZED_USER_IDS = [4,5]