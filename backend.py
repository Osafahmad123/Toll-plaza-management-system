import sqlite3
from datetime import datetime

class TollPlaza:
    def __init__(self):
        self.conn = sqlite3.connect('toll_plaza.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS vehicles (
                                id INTEGER PRIMARY KEY,
                                name TEXT
                            )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS vehicles_rate (
                                id INTEGER PRIMARY KEY,
                                vehicle_id INTEGER,
                                rate INTEGER,
                                FOREIGN KEY(vehicle_id) REFERENCES vehicles(id)
                            )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS passenger_data (
                                id INTEGER PRIMARY KEY,
                                vehicle_id INTEGER,
                                number_plate TEXT,
                                rate INTEGER,
                                passage_time TEXT,
                                FOREIGN KEY(vehicle_id) REFERENCES vehicles(id)
                            )''')
        self.conn.commit()

    def add_vehicle(self, name):
        self.cursor.execute('''INSERT INTO vehicles (name) VALUES (?)''', (name,))
        self.conn.commit()

    def add_or_update_vehicle_rate(self, vehicle_name, rate):
        vehicle_id = self.get_vehicle_id(vehicle_name)
        if vehicle_id:
            self.cursor.execute('''INSERT OR REPLACE INTO vehicles_rate (vehicle_id, rate) VALUES (?, ?)''', (vehicle_id, rate))
            self.conn.commit()
            return "Rate updated successfully"
        else:
            return "Vehicle not found"

    def get_vehicle_id(self, name):
        self.cursor.execute('''SELECT id FROM vehicles WHERE name=?''', (name,))
        vehicle = self.cursor.fetchone()
        if vehicle:
            return vehicle[0]
        else:
            return None

    def get_vehicle_rate(self, name):
        vehicle_id = self.get_vehicle_id(name)
        if vehicle_id:
            self.cursor.execute('''SELECT rate FROM vehicles_rate WHERE vehicle_id=?''', (vehicle_id,))
            rate = self.cursor.fetchone()
            if rate:
                return rate[0]
        return None

    def register_passage(self, vehicle_name, number_plate):
        vehicle_id = self.get_vehicle_id(vehicle_name)
        rate = self.get_vehicle_rate(vehicle_name)
        if vehicle_id and rate:
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute('''INSERT INTO passenger_data (vehicle_id, number_plate, rate, passage_time)
                                VALUES (?, ?, ?, ?)''', (vehicle_id, number_plate, rate, current_time))
            self.conn.commit()
            return "Passage registered successfully"
        else:
            return "Vehicle or rate not found"

    def search_passenger_data(self, number_plate):
        self.cursor.execute('''SELECT vehicles.name, passenger_data.number_plate, passenger_data.rate, passenger_data.passage_time
                                FROM passenger_data
                                JOIN vehicles ON passenger_data.vehicle_id = vehicles.id
                                WHERE passenger_data.number_plate=?''', (number_plate,))
        data = self.cursor.fetchall()
        if data:
            return data
        else:
            return "Passenger data not found"

    def passage_data(self):
        self.cursor.execute('''SELECT vehicles.name, passenger_data.number_plate, passenger_data.rate, passenger_data.passage_time
                               FROM passenger_data
                               JOIN vehicles ON passenger_data.vehicle_id = vehicles.id''')
        data = self.cursor.fetchall()
        return data
    
    def all_vehicle(self):
        self.cursor.execute('''SELECT name FROM vehicles''')
        names = self.cursor.fetchall()
        return [name[0] for name in names]
    
    def close_connection(self):
        self.conn.close()
