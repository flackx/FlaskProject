from flask import Flask, render_template, request, redirect, url_for, session, flash
from flaskext.mysql import MySQL
from service import UserService, ImageService
from Resources.config import DatabaseConfig
import os
from werkzeug.utils import secure_filename
from functools import wraps

app = Flask(__name__, static_folder='static')


UPLOAD_FOLDER = 'Resources/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['MYSQL_DATABASE_HOST'] = DatabaseConfig.HOST
app.config['MYSQL_DATABASE_PORT'] = DatabaseConfig.PORT
app.config['MYSQL_DATABASE_USER'] = DatabaseConfig.USER
app.config['MYSQL_DATABASE_PASSWORD'] = DatabaseConfig.PASSWORD
app.config['MYSQL_DATABASE_DB'] = DatabaseConfig.DB

mysql = MySQL()
mysql.init_app(app)

user_service = UserService(mysql)
image_service = ImageService(mysql)


# Decorator function to check if the user is authenticated
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('You need to login first!')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle the login form submission
        username = request.form['username']
        password = request.form['password']

        # Verify login credentials against the database
        user = user_service.verify_credentials(username, password)

        if user:
            # If login is successful, store user session data
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('home'))
        else:
            # If login is unsuccessful, redirect back to the login page with an error message
            flash('Invalid username or password!')
            return redirect(url_for('login'))

    # Render the login form
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle the registration form submission
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Save the user data to the database
        user_service.register_user(username, password, email)

        # Redirect to a success page or another route
        return redirect(url_for('home'))

    # Render the registration form
    return render_template('register.html')


@app.route('/gallery')
@login_required
def gallery():
    # Retrieve image paths from the database
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT filepath FROM images")
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    # Create a list of image paths
    image_paths = [row[0] for row in data]

    return render_template('gallery.html', image_paths=image_paths)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        # Check if file is present in the request
        if 'file' not in request.files:
            flash("No file selected!")
            return redirect(request.url)

        file = request.files['file']

        # Check if the file is empty
        if file.filename == '':
            flash("No file selected!")
            return redirect(request.url)

        # Check if the file extension is allowed
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            # Save the image path to the database
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "INSERT INTO images (filename, filepath) VALUES (%s, %s)"
            cursor.execute(query, (filename, filepath))
            conn.commit()
            cursor.close()
            conn.close()

            flash("Image uploaded successfully!")
            return redirect(url_for('gallery'))
        else:
            flash("Invalid file extension!")
            return redirect(request.url)

    return render_template('upload.html')


if __name__ == '__main__':
    app.run()
