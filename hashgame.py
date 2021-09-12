from flask import Flask, render_template
import hashlib
import json

app = Flask(__name__)

with open("mappings.json") as mappings_file:
    mappings = {int(k):v for (k,v) in json.load(mappings_file).items()}

@app.route("/")
def index():
    return "Index page"


@app.route("/play/<string:guess>")
def play(guess):
    digest = hashlib.sha1(guess.encode()).hexdigest()
    level = digest.count("7")
    message_num = int(digest, 16)
    num_descriptions = len(mappings[level]["Descriptions"])
    if level > 7:
        level = 7
    tier = mappings[level]["Tier"]
    description = mappings[level]["Descriptions"][message_num % num_descriptions]
    image_num = message_num % 4 + 1
    if level == 7:
        image_num = 1
    image_url = f"/static/img/{tier}/{image_num}.png"
    return render_template("play.html", tier=tier, description=description, image_url=image_url)