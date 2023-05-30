from flask import flash

class UserService:
    def __init__(self, mysql):
        self.mysql = mysql

    def register_user(self, username, password, email):
        conn = self.mysql.connect()
        cursor = conn.cursor()
        query = "INSERT INTO users (Username, Password, Email) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, password, email))
        conn.commit()
        cursor.close()
        conn.close()

    def verify_credentials(self, username, password):
        conn = self.mysql.connect()
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE Username = %s AND Password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user

class ImageService:
    def __init__(self, mysql):
        self.mysql = mysql

    def save_image(self, file):
        # Get the filename and file data
        filename = file.filename
        file_data = file.read()

        # Save the image data to the database
        conn = self.mysql.connect()
        cursor = conn.cursor()
        query = "INSERT INTO images (filename, filedata) VALUES (%s, %s)"
        cursor.execute(query, (filename, file_data))
        conn.commit()
        cursor.close()
        conn.close()

        flash("Image uploaded successfully!")

    def get_images(self):
        conn = self.mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM images")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data

