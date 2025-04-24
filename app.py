import os
from flask import Flask, render_template, request, send_file, redirect, url_for, flash, Response
from flask_login import LoginManager, login_required, logout_user, login_user

from User import User
DEFAULT_PATH ="C:\\"

login_manager = LoginManager()
app = Flask(__name__)  # Create a Flask instance
login_manager.init_app(app)

app.secret_key = "Secret Key" # Put your secret key here
@app.route('/hello/<name>')
def hello(name):
    return f'Hello, {name}!'
@app.route('/')
def home():
    return render_template('index.html', message='Welcome to my Web Server!', dirs=getDirs(), files=getFiles(), path=DEFAULT_PATH)

@app.route('/browse')
def browse():
    directoryPath = request.args.get('directory')
    if directoryPath:
        directoryName = directoryPath.split('/')[-1]
        return render_template('index.html', message=f'Contents of {directoryName}', dirs=getDirs(directoryPath), files=getFiles(directoryPath), path=directoryPath)
    return render_template('index.html', message='Welcome to my Web Server!', dirs=getDirs(), files=getFiles(), path=DEFAULT_PATH)

@app.route('/download')
def download():
    filePath = request.args.get('file')
    if filePath:
        # return send_file(filePath, as_attachment=True) # Always Download
        return send_file(filePath, as_attachment=False) # Display files .mp4 .jpg etc in browser
    return redirect(request.url)

@app.post('/upload')
@login_required
def upload():
    if 'file' not in request.files:
        flash('No file part')
        return Response(status=204)
    file = request.files['file']
    path = request.form.get('path')
    if file.filename == '':
        flash('No selected file')
        return Response(status=204)
    if file:
        file.save(os.path.join(path, file.filename))
    return render_template('index.html', message=f'Contents of {path}', dirs=getDirs(path),
                           files=getFiles(path), path=path)


@app.route('/login')
def form():
    return render_template('login.html')
@app.post("/login")
def login():
    user = User.get(request.form.get("email"))

    if user is None or user.password != request.form.get("password"):
        flash('Invalid Login Credentials')
        return redirect(url_for("login"))


    login_user(user)
    return redirect(url_for("home"))

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    return f'Hello, {name}!'


def getFiles(path=DEFAULT_PATH):
    return [f for f in os.scandir(path) if os.path.isfile(f)]
def getDirs(path=DEFAULT_PATH):
    return [f for f in os.scandir(path) if os.path.isdir(f)]


if __name__ == "__main__":
    app.run(debug=True)  # Run the app in debug mode

