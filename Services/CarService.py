class CarService:
    def __init__(self, mysql):
        self.mysql = mysql

    def create_car_table(self):
        conn = self.mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cars (
                id INT AUTO_INCREMENT PRIMARY KEY,
                make VARCHAR(255) NOT NULL,
                model VARCHAR(255) NOT NULL,
                year INT,
                description TEXT,
                image_path VARCHAR(255),
                price DECIMAL(10, 2),
                phone_number VARCHAR(20)
            )
        """)
        cursor.close()
        conn.close()

    def get_all_cars(self):
        conn = self.mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, make, model, year, description, image_path, price, phone_number FROM cars")
        cars = cursor.fetchall()
        cursor.close()
        conn.close()

        # Convert tuples to dictionaries
        cars_list = []
        for car in cars:
            car_dict = {
                'id': car[0],
                'make': car[1],
                'model': car[2],
                'year': car[3],
                'description': car[4],
                'image_path': car[5],
                'price': car[6],
                'phone_number': car[7]
            }
            cars_list.append(car_dict)

        return cars_list

    def save_car(self, make, model, year, description, image_path, price, phone_number):
        conn = self.mysql.connect()
        cursor = conn.cursor()

        # Check if the 'cars' table exists, and create it if not
        cursor.execute("SHOW TABLES LIKE 'cars'")
        table_exists = cursor.fetchone()
        if not table_exists:
            self.create_car_table()

        cursor.execute(
            "INSERT INTO cars (make, model, year, description, image_path, price, phone_number) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (make, model, year, description, image_path, price, phone_number),
        )
        conn.commit()
        cursor.close()
        conn.close()

    def get_car_by_id(self, car_id):
        connection = self.mysql.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM cars WHERE id = %s", (car_id,))
        car = cursor.fetchone()
        cursor.close()
        connection.close()

        if car:
            # Convert the car tuple to a dictionary
            car_dict = {
                'id': car[0],
                'make': car[1],
                'model': car[2],
                'year': car[3],
                'description': car[4],
                'image_path': car[5],
                'price': car[6],
                'phone_number': car[7]
            }
            return car_dict
        else:
            # Handle the case where the car with the given ID is not found
            return None
