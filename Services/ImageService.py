import os


class ImageService:
    def __init__(self, mysql):
        self.mysql = mysql

    def save_image_path(self, image_path):
        conn = self.mysql.connect()
        cursor = conn.cursor()

        # Create the table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS images (
                id INT AUTO_INCREMENT PRIMARY KEY,
                filepath VARCHAR(255)
            )
        """)

        # Extract the relative image path
        relative_path = image_path.split('static/')[1]

        # Insert the relative image path
        cursor.execute("INSERT INTO images (filepath) VALUES (%s)", (relative_path,))

        conn.commit()
        cursor.close()
        conn.close()

    def get_image_paths(self):
        conn = self.mysql.connect()
        cursor = conn.cursor()

        # Check if the table exists
        cursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_name = 'images'
        """)
        table_exists = cursor.fetchone()[0] == 1

        if table_exists:
            cursor.execute("SELECT filepath FROM images")
            data = cursor.fetchall()
            image_paths = [os.path.join('static', row[0]) for row in data]
        else:
            image_paths = []  # Return an empty list if the table doesn't exist

        cursor.close()
        conn.close()

        return image_paths
