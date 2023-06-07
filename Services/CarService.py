class CarService:
    def __init__(self, mysql):
        self.mysql = mysql

    def get_all_cars(self):
        conn = self.mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, make, model, year, description, image_path FROM cars")
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
                'image_path': car[5]
            }
            cars_list.append(car_dict)

        return cars_list

    def save_car(self, model, description, image_path, make, year):
        conn = self.mysql.connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO cars (make, model, year, description, image_path) VALUES (%s, %s, %s, %s, %s)",
            (make, model, year, description, image_path),
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
                'image_path': car[5]
            }
            return car_dict
        else:
            # Handle the case where the car with the given ID is not found
            return None
