import os

from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from werkzeug.utils import secure_filename

# where uploads will be stored
UPLOAD_FOLDER = "./uploads"

# creates upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# a few sane extensions to ban
BANNED_EXTENSIONS = {"exe", "app", "deb"}

app = Flask(__name__, static_url_path="", static_folder="static")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    """ Checks if file extension is allowed """
    return (
        "." in filename and filename.rsplit(".", 1)[1].lower() not in BANNED_EXTENSIONS
    )


@app.route("/")
def index():
    """ Serves index.html """
    return app.send_static_file("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files or request.files.filename == "":
        app.logger.error("no file attached")
        return jsonify({})

    file = request.files
    allowed = allowed_file(file.filename)

    if file and allowed:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        # return redirect(url_for("uploaded_file", filename=filename)) # no need to redirect automatically

        return jsonify({"url": url_for("uploaded_file", filename=filename)})


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run()
