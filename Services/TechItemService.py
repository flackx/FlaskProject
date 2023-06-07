from flaskext.mysql import MySQL
class TechItemService:
    def __init__(self, mysql):
        self.mysql = mysql

    def save_tech_item(self, name, brand, description, image_path, price, phone_number):
        conn = self.mysql.connect()
        cursor = conn.cursor()

        try:
            query = "INSERT INTO tech_items (name, brand, description, image_path, price, phone_number) " \
                    "VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (name, brand, description, image_path, price, phone_number))
            conn.commit()
        except Exception as e:
            print("Error saving tech item:", e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def get_all_tech_items(self):
        conn = self.mysql.connect()
        cursor = conn.cursor()

        try:
            query = "SELECT * FROM tech_items"
            cursor.execute(query)
            tech_items = cursor.fetchall()
            return tech_items
        except Exception as e:
            print("Error retrieving tech items:", e)
        finally:
            cursor.close()
            conn.close()

    def get_tech_item_by_id(self, tech_item_id):
        conn = self.mysql.connect()
        cursor = conn.cursor()

        try:
            query = "SELECT * FROM tech_items WHERE id = %s"
            cursor.execute(query, (tech_item_id,))
            tech_item = cursor.fetchone()
            return tech_item
        except Exception as e:
            print("Error retrieving tech item:", e)
        finally:
            cursor.close()
            conn.close()
