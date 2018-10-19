import os
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
from PIL import Image
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '\\upload\\'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_file', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            sourcepath = os.path.join('upload', filename)
            destinationpath = os.path.join('upload', "file.pdf")
            file.save(sourcepath)
            # storing image path
            img_path = sourcepath
            # storing pdf path
            pdf_path = destinationpath
            # opening image
            image = Image.open(img_path)
            # converting into chunks using img2pdf
            pdf_bytes = img2pdf.convert(image.filename)
            # opening or creating pdf file
            file = open(pdf_path, "wb")
            # writing pdf files with chunks
            file.write(pdf_bytes)
            # closing image file
            image.close()
            # closing pdf file
            file.close()
            # output
            print("Successfully made pdf file")
            return send_from_directory(directory='upload',
                                       filename='file.pdf',
                                       mimetype='application/pdf')


if __name__ == '__main__':
    app.run(debug=True)
