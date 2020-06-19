from flask import Flask, jsonify, render_template, request, url_for
import sqlite3

app = Flask(__name__, static_folder="static")


@app.route("/")
def index():
    return app.send_static_file("index.html")


if __name__ == "__main__":
    app.run()
