from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder="templates")


@app.route('/')
def landing():
    return render_template("home.html")