from flask import Flask, render_template, request, redirect, url_for
import db
import requests
import json

ROOT_URL = "https://www.googleapis.com/books/v1/volumes"
API_KEY = "AIzaSyAVIQN19bXuCQsEAVElCeSS9hqiHouK-R4"
params = {"maxResults": 40}

app = Flask(__name__)
results = "harry"


def search_title(name):
    name = "+".join(name.split(" "))
    r = requests.get(ROOT_URL + "?q=" + name + "&key=" + API_KEY)
    return r.json()["items"]


@app.route("/hello", methods=["GET", "POST"])
def hello_world():
    return "hello world"


@app.route("/", methods=["GET", "POST"])
def home_page():
    global results
    if request.method == "POST" and request.form["search-bar"]:
        results = search_title(request.form["search-bar"])
    return render_template("index.html", results=results)


@app.route("/favourites")
def favourites():
    all = db.get_all()
    return render_template("favs.html", all=all)


@app.route("/add/<string:id>", methods=["POST"])
def add(id):
    if request.method == "POST":
        book = list(filter(lambda b: b["id"] == id, results))[0]
        db.add_book(book)
    return ("", 204)


@app.route("/delete/<string:id>", methods=["DELETE"])
def delete(id):
    if request.method == "DELETE":
        db.delete_book(id)
    return ("", 204)


if __name__ == "__main__":
    app.run(debug=True)
