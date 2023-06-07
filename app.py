from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from flaskext.mysql import MySQL
from wtforms import FileField, StringField, TextAreaField, IntegerField, DecimalField
from wtforms.validators import DataRequired, NumberRange

from Services.HouseService import HouseService
from Services.ImageService import ImageService
from Services.TechItemService import TechItemService
from Services.config import DatabaseConfig
import os
from werkzeug.utils import secure_filename
from functools import wraps
from Services.CarService import CarService
from Services.UserService import UserService
from flask import Flask, render_template


app = Flask(__name__, static_folder='static')

app.config['UPLOAD_FOLDER'] = 'static/images'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['SECRET_KEY'] = 'your-secret-key'
app.config['MYSQL_DATABASE_HOST'] = DatabaseConfig.HOST
app.config['MYSQL_DATABASE_PORT'] = DatabaseConfig.PORT
app.config['MYSQL_DATABASE_USER'] = DatabaseConfig.USER
app.config['MYSQL_DATABASE_PASSWORD'] = DatabaseConfig.PASSWORD
app.config['MYSQL_DATABASE_DB'] = DatabaseConfig.DB

mysql = MySQL()
mysql.init_app(app)

car_service = CarService(mysql)
user_service = UserService(mysql)
image_service = ImageService(mysql)
house_service = HouseService(mysql)
tech_item_service = TechItemService(mysql)



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
def default():
    return redirect(url_for('login'))


@login_required
@app.route('/home', methods=['GET'])
def home():
    # Read the username from the session
    username = session.get('username')

    # Retrieve all cars from the database
    cars = car_service.get_all_cars()

    return render_template('home.html', username=username, cars=cars)

@app.route('/car_details/<int:car_id>')
def car_details(car_id):
    car = car_service.get_car_by_id(car_id)
    if car:
        return render_template('car_details.html', car=car)
    else:
        flash('Car not found!')
        return redirect(url_for('home'))

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
            # If login is unsuccessful, render the login page with an error message
            error = 'Invalid username or password!'
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/logout')
def logout():
    # Logic for logging out the user
    # This can include clearing session data, redirecting to the login page, etc.
    return 'Logged out successfully'  # Placeholder response, customize as needed

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        user_service.register_user(username, password, email)

        return redirect(url_for('home'))

    return render_template('register.html')

@app.route('/gallery')
@login_required
def gallery():
    cars = car_service.get_all_cars()

    return render_template('gallery.html', cars=cars)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class UploadFormCar(FlaskForm):
    make = StringField('Make', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    image = FileField('Image', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])


@login_required
@app.route('/uploadcar', methods=['GET', 'POST'])
def uploadcar():
    form = UploadFormCar()
    if form.validate_on_submit():
        image_file = form.image.data
        filename = secure_filename(image_file.filename)
        image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        image_service.save_image_path(image_path)
        make = form.make.data
        model = form.model.data
        year = form.year.data
        description = form.description.data
        price = form.price.data
        phone_number = form.phone_number.data
        car_service.save_car(make, model, year, description, image_path, price, phone_number)

        flash('Car uploaded successfully!')
        return redirect(url_for('home'))

    return render_template('uploadcar.html', form=form, car=None)


@app.route('/houses', methods=['GET'])
def houses():
    # Read the username from the session
    username = session.get('username')

    # Retrieve all houses from the database
    houses = house_service.get_all_houses()

    return render_template('houses.html', username=username, houses=houses)

@app.route('/house_details/<int:house_id>')
def house_details(house_id):
    house = house_service.get_house_by_id(house_id)
    if house:
        return render_template('house_details.html', house=house)
    else:
        flash('House not found!')
        return redirect(url_for('houses'))

class UploadFormHouse(FlaskForm):
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    bedrooms = IntegerField('Bedrooms', validators=[DataRequired()])
    bathrooms = IntegerField('Bathrooms', validators=[DataRequired()])
    area = StringField('Area', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    image = FileField('Image', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])



@login_required
@app.route('/uploadhouse', methods=['GET', 'POST'])
def uploadhouse():
    form = UploadFormHouse()
    if form.validate_on_submit():
        image_file = form.image.data
        filename = secure_filename(image_file.filename)
        image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            bedrooms = int(form.bedrooms.data)
        except ValueError:
            flash('Please enter a valid number for bedrooms.')
            return redirect(url_for('uploadhouse'))

        image_service.save_image_path(image_path)
        address = form.address.data
        city = form.city.data
        bedrooms = form.bedrooms.data
        bathrooms = form.bathrooms.data
        area = form.area.data
        description = form.description.data
        price = form.price.data
        phone_number = form.phone_number.data
        house_service.save_house(address, city, bedrooms, bathrooms, area, description, image_path, price, phone_number)

        flash('House uploaded successfully!')
        return redirect(url_for('houses'))

    return render_template('uploadhouse.html', form=form)


class UploadFormTech(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    brand = StringField('Brand', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    image = FileField('Image', validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png'])])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)])
    phone_number = StringField('Phone Number', validators=[DataRequired()])


@app.route('/uploadtech', methods=['GET', 'POST'])
def uploadtech():
    form = UploadFormTech()
    if form.validate_on_submit():
        image_file = form.image.data
        filename = secure_filename(image_file.filename)
        image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        tech_item_service.save_tech_item(
            form.name.data,
            form.brand.data,
            form.description.data,
            image_path,
            form.price.data,
            form.phone_number.data
        )

        flash('Tech item uploaded successfully!')
        return redirect(url_for('home'))

    return render_template('uploadtech.html', form=form)

@app.route('/techitems', methods=['GET'])
def tech_items():
    # Retrieve all tech items from the database
    tech_items = tech_item_service.get_all_tech_items()

    return render_template('techitems_details.html', tech_items=tech_items)





if __name__ == '__main__':
    app.run()