import os
os.environ['KMP_DUPLICATE_LIB_OK'] = "True"
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
from tensorflow.keras.models import load_model
from flask import Flask, flash, redirect, render_template, request, url_for

model = load_model("./models/model.h5")
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = "static/uploads/"


@app.route('/')
def dashboard():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def upload():
    if "image" not in request.files:
        flash("No image uploaded")
        return redirect(request.url)
    # Upload Image
    image = request.files['image']
    if image.filename == "":
        flash("No image selected")
        return redirect(request.url)
    im_name = image.filename
    image_path = os.path.join(app.config["UPLOAD_FOLDER"], im_name)
    image.save(image_path)

    img = open(os.path.join(app.config['UPLOAD_FOLDER'], im_name))

    return render_template('index.html',
                           filename=im_name,
                           prediction_text=1)


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.errorhandler(500)
def server_error(error):
    return render_template('error.html'), 500


if __name__ == "__main__":
    app.run(debug=True)
