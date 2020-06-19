import os
from hashlib import blake2b

from flask import (Flask, jsonify, redirect, render_template, request,
                   send_from_directory, url_for)
from werkzeug.utils import secure_filename

MAX_FILE_SIZE = 1440000  # 1.44mb in bytes

# where uploads will be stored
UPLOAD_FOLDER = "./uploads"

# creates upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# a few sane extensions to ban
BANNED_EXTENSIONS = {"exe", "app", "deb", "msi"}

app = Flask(__name__, static_url_path="", static_folder="static")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def get_ext(filename):
    """ Get file extension """
    return filename.rsplit(".", 1)[1].lower()


def allowed_file(filename):
    """ Checks if file extension is allowed """
    return "." in filename and get_ext(filename) not in BANNED_EXTENSIONS


@app.route("/")
def index():
    """ Serves index.html """
    return app.send_static_file("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    """ Upload a given file """
    file = request.files["file"]
    if "file" not in request.files or file == "":
        app.logger.error("no file attached")
        return jsonify({})

    file.seek(0, 2)  # go to the end of the file
    size = file.tell()  # find how many bytes are there
    print(size)
    allowed = allowed_file(file.filename) and size <= MAX_FILE_SIZE

    if file and allowed:
        hash3 = blake2b(digest_size=20)
        hash3.update(file.read())
        filename = hash3.hexdigest() + "." + get_ext(file.filename)
        file.seek(0)  # required to save file properly since read() reads it all
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        # return redirect(url_for("uploaded_file", filename=filename)) # no need to redirect automatically

        return jsonify({"url": url_for("uploaded_file", filename=filename)})

    else:
        return jsonify({"url": "Error: file too large"})


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run()
