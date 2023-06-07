class HouseService:
    def __init__(self, mysql):
        self.mysql = mysql

    def create_house_table(self):
        conn = self.mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS houses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                address VARCHAR(255) NOT NULL,
                city VARCHAR(255) NOT NULL,
                bedrooms INT,
                bathrooms INT,
                area DECIMAL(10, 2),
                description TEXT,
                image_path VARCHAR(255),
                price DECIMAL(10, 2),
                phone_number VARCHAR(20)
            )
        """)
        cursor.close()
        conn.close()

    def get_all_houses(self):
        conn = self.mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, address, city, bedrooms, bathrooms, area, description, image_path, price, phone_number FROM houses")
        houses = cursor.fetchall()
        cursor.close()
        conn.close()

        # Convert tuples to dictionaries
        houses_list = []
        for house in houses:
            house_dict = {
                'id': house[0],
                'address': house[1],
                'city': house[2],
                'bedrooms': house[3],
                'bathrooms': house[4],
                'area': house[5],
                'description': house[6],
                'image_path': house[7],
                'price': house[8],
                'phone_number': house[9]
            }
            houses_list.append(house_dict)

        return houses_list

    def save_house(self, address, city, bedrooms, bathrooms, area, description, image_path, price, phone_number):
        conn = self.mysql.connect()
        cursor = conn.cursor()

        # Check if the 'houses' table exists, and create it if not
        cursor.execute("SHOW TABLES LIKE 'houses'")
        table_exists = cursor.fetchone()
        if not table_exists:
            self.create_house_table()

        cursor.execute(
            "INSERT INTO houses (address, city, bedrooms, bathrooms, area, description, image_path, price, phone_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (address, city, bedrooms, bathrooms, area, description, image_path, price, phone_number),
        )
        conn.commit()
        cursor.close()
        conn.close()

    def get_house_by_id(self, house_id):
        connection = self.mysql.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM houses WHERE id = %s", (house_id,))
        house = cursor.fetchone()
        cursor.close()
        connection.close()

        if house:
            # Convert the house tuple to a dictionary
            house_dict = {
                'id': house[0],
                'address': house[1],
                'city': house[2],
                'bedrooms': house[3],
                'bathrooms': house[4],
                'area': house[5],
                'description': house[6],
                'image_path': house[7],
                'price': house[8],
                'phone_number': house[9]
            }
            return house_dict
        else:
            # Handle the case where the house with the given ID is not found
            return None
