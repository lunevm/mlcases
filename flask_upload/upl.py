import numpy as np
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from cv2 import imread, inRange, countNonZero
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = 'super secret key'

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


@app.route("/alert")
def alert():
    return '<h1>Alert Page (to be continued)</h1>'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route("/", methods=['GET', 'POST'])
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('alert'))
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('alert'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            pixels = count_pixels(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('result_page.html', posts = pixels)

    return render_template('upload_page.html')
    #return redirect(url_for('uploaded_file',filename=filename))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


def count_pixels(filename):
    img = imread(filename)

    black_pixel = np.array([0,0,0], np.uint8)
    blacks = inRange(img, black_pixel, black_pixel)
    count_blacks = countNonZero(blacks)

    white_pixel = np.array([255,255,255], np.uint8)
    whites = inRange(img, white_pixel, white_pixel)
    count_whites = countNonZero(whites)

    if count_whites > count_blacks:
        diff = 'Белых пикселей больше'
    elif count_blacks > count_whites:
        diff = 'Черных пикселей больше'
    else:
        diff = 'Количество черных и белых пикселей одинаковое'

    return {'black':count_blacks, 'white':count_whites, 'diff':diff}


if __name__ == '__main__':
    app.run(debug=True)
