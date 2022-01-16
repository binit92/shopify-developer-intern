import os
from wsgiref.util import request_uri
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# maximum size is 16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

# only allowed types are png, jpg, jpeg and gif
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



#references: https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist("file")
        print("files: ", files)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        for file in files:
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                #return redirect(url_for('download_file', name=filename))
        return "Images have been uploaded" , 200
    return

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route("/")
def hello():
    return render_template('index.html')

if __name__ == "__main__":
    # use of on-the-fly certificates for HTTPS
    # commenting it for now as hosting in localhost throws warning
    # ref: https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https

    #app.run(ssl_context='adhoc', debug = True)
    #app.run(debug = True)
    app.run(ssl_context=('cert.pem', 'key.pem'))
        