import sqlite3
import json
import random
import datetime

DATABASE = "foodiespot.db"

def create_connection():
    return sqlite3.connect(DATABASE)

def init_db():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            cuisine TEXT NOT NULL,
            total_seats INTEGER NOT NULL
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservations(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id INTEGER,
            date TEXT NOT NULL,
            time_slot INTEGER NOT NULL,
            seats_booked INTEGER NOT NULL,
            booking_email TEXT NOT NULL
        );
    """)

    conn.commit()
    conn.close()



def populate_restaurants():
    """ Populate the restaurants table with sample data. """
    conn = create_connection()
    cursor = conn.cursor()

    # Sample restaurant data
    restaurants = [
        ("Spice Haven", "Downtown", "Indian", 50),
        ("Pasta Paradise", "Midtown", "Italian", 40),
        ("Sushi Zen", "Uptown", "Japanese", 30),
        ("BBQ Smokehouse", "Riverside", "BBQ", 60),
        ("Vegan Delight", "City Center", "Vegan", 35),
        ("Taco Fiesta", "East Side", "Mexican", 45),
        ("Burger Junction", "West End", "American", 55),
        ("Mediterranean Bliss", "Harbor", "Mediterranean", 25),
        ("French Elegance", "Old Town", "French", 20),
        ("Seafood Haven", "Coastal", "Seafood", 40),
        ("Dim Sum Palace", "Chinatown", "Chinese", 50),
        ("Steakhouse Supreme", "South Side", "Steakhouse", 35),
        ("Fusion Feast", "Tech Park", "Fusion", 30),
        ("Dosa Corner", "Little India", "South Indian", 40),
        ("Biryani Central", "Market District", "Indian", 60),
        ("Pizza Heaven", "Suburbia", "Italian", 45),
        ("Kebab Kingdom", "Downtown", "Middle Eastern", 30),
        ("Waffle Wonderland", "University Area", "Desserts", 25),
        ("Healthy Bites", "Corporate Hub", "Healthy", 35),
        ("Tapas Bar", "City Center", "Spanish", 40),
    ]

    # Insert data
    cursor.executemany(
        "INSERT INTO restaurants (name, location, cuisine, total_seats) VALUES (?, ?, ?, ?)",
        restaurants
    )

    conn.commit()
    conn.close()
    print("✅ Restaurant database populated successfully!")


def populate_reservations():
    """Populate the reservations table with sample data, using the restaurant name to fetch the corresponding restaurant_id."""
    conn = create_connection()
    cursor = conn.cursor()

    # Sample restaurant names (must exist in the 'restaurants' table)
    restaurant_names = [
        "Spice Haven", "Pasta Paradise", "Sushi Zen", "BBQ Smokehouse", 
        "Vegan Delight", "Taco Fiesta", "Burger Junction", "Mediterranean Bliss", 
        "French Elegance", "Seafood Haven", "Dim Sum Palace", "Steakhouse Supreme", 
        "Fusion Feast", "Dosa Corner", "Biryani Central", "Pizza Heaven", 
        "Kebab Kingdom", "Waffle Wonderland", "Healthy Bites", "Tapas Bar"
    ]

    # Dates: Today and tomorrow
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    # Sample time slots (you can adjust based on your data)
    time_slots = ["12:00 PM", "3:00 PM", "6:00 PM", "8:00 PM"]

    # Number of reservations to populate
    num_reservations = 30  # Adjust the number of reservations as needed

    # Generate random reservations
    reservation_data = []
    for i in range(num_reservations):
        restaurant_name = random.choice(restaurant_names)
        
        # Fetch the restaurant_id based on the name from the 'restaurants' table
        cursor.execute("SELECT * FROM restaurants WHERE name = ?", (restaurant_name,))
        result = cursor.fetchone()

        if result:  # Ensure the restaurant exists
            restaurant_id = result[0]
        else:
            continue  # Skip if no valid restaurant is found

        # Randomly choose between today and tomorrow
        date = today if random.choice([True, False]) else tomorrow
        time_slot = random.choice(time_slots)
        seats_needed = random.randint(1, int(result[4])+1)  # Random seats between 1 and 6

        reservation_data.append((restaurant_id, date, time_slot, seats_needed,f"user{i}@gmail.com"))

    # Insert data into the reservations table
    cursor.executemany(
        "INSERT INTO reservations (restaurant_id, date, time_slot, seats_booked,booking_email) VALUES (?, ?, ?, ?,?)",
        reservation_data
    )

    conn.commit()
    conn.close()
    print("✅ Reservations database populated successfully!")

if __name__ == "__main__":
    init_db()
    populate_restaurants()
    populate_reservations()
    
    print("Database initialized!")
