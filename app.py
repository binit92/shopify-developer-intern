import os
from wsgiref.util import request_uri
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from db import db_init, db
from models import Img

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# maximum size is 16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

# SQLAlchemy config. Read more: https://flask-sqlalchemy.palletsprojects.com/en/2.x/
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///img.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)

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
        # checkbox for private/public permission
        private_list = request.form.getlist('p_checkbox')
        print("--> checkbox: ", private_list)
        private = False
        if "private" in private_list:
            private = True

        files = request.files.getlist("file")
        print("--> files: ", files)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        for file in files:
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                print("--> path is : ", path)
                print("--> private: ", private)
                file.save(path)
                #return redirect(url_for('download_file', name=filename))

                # save entries into db
                try:
                    print("filename: ", filename)
                    print("mimetype: ", file.mimetype)
                    print("path: ", path)
                    print("private: ",private)
                    img = Img(name = filename,mimetype = file.mimetype, file_location = path, private_img = private )
                    print(img)
                    db.session.add(img)
                    print("add image")
                    db.session.commit()
                    print("db committed")
                except:
                    print("error occurred while saving into db")
        #return "Images have been uploaded" , 200
        return redirect('/')
    return

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route("/" , methods = ['POST', 'GET'])
def index():
    #print("index: ")
    if request.method == 'POST':
        #print("POST request")
        return redirect('/')
    else:
        try:
            all_image = Img.query.all()
            #for i in all_image:
            #    print(i.name, i.file_location, i.private_img)
        except:
            print("error in getting all image details ")
        return render_template('index.html', all_image = all_image)


if __name__ == "__main__":
    # use of on-the-fly certificates for HTTPS
    # commenting it for now as hosting in localhost throws warning
    # ref: https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https

    #app.run(ssl_context='adhoc', debug = True)
    #app.run(debug = True)
    app.run(ssl_context=('cert.pem', 'key.pem'))
        