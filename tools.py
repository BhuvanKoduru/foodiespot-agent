from db import create_connection
import streamlit as st
import datetime

def get_locations():
    """Fetch all restaurant locations from the database. If the user wants all the locations, use this tool ONLY
    
    Returns:
        list[dict]: A list of dictionaries, each containing:
            - name (str): Restaurant name.
            - location (str): Geographic location.
            - cuisine (str): Type of cuisine offered.
            - total_seats (int): Number of total seats.
    """
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name, location, cuisine, total_seats FROM restaurants")
    results = cursor.fetchall()
    conn.close()

    return [{"name": row[0], "location": row[1], "cuisine": row[2], "total_seats": row[3]} for row in results]



# Function to get the total seats booked for a specific date, restaurant, and slot
def get_total_seats_booked(date, restaurant_id, slot):
    conn = create_connection()
    cursor = conn.cursor()
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    date = today if date == "Today" else tomorrow
    query = """
        SELECT SUM(seats_booked)
        FROM reservations
        WHERE date = ? AND restaurant_id = ? AND time_slot = ?
        GROUP BY restaurant_id, date, time_slot
    """

    cursor.execute(query, (date, restaurant_id, slot))
    result = cursor.fetchone()
    print(result)
    conn.close()

    return result[0] if result else 0

def find_alternate_restaurants(date, slot, seats_needed):
      # List of available restaurants
    """Confirm a reservation and update the database."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM restaurants")
    results = cursor.fetchall()
    available_list=[]
    if results:
        for result in results:# Ensure the restaurant exists
            id = result[0]
            total=result[4]
            name=result[1]
            booked=get_total_seats_booked(date,id,slot)
            if(total-booked>=int(seats_needed)):
                available_list.append(name)
    if(len(available_list)>0):
        return (f"Here are other avaialble restaurants: {" ".join(available_list)}. List them to the user.")
    return ("There are no available retuarants at the moment")
def confirm_reservation(location, date,slot, seats_needed):
    """Confirm a reservation and update the database."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM restaurants WHERE name = ?", (location,))
    result = cursor.fetchone()

    if result:  # Ensure the restaurant exists
        id = result[0]
        total=result[4]
    # Reduce available seats
    
    # dat,id,slot
    booked=get_total_seats_booked(date,id,slot)
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    date = today if date == "Today" else tomorrow
    if(total-booked>=int(seats_needed)):
        cursor.execute(
                    "INSERT INTO reservations (restaurant_id, date, time_slot, seats_booked,booking_email) VALUES (?, ?, ?, ?,?)",
            (id,date,slot,seats_needed, st.session_state['email']),
        )
        conn.commit()
        conn.close()
        
        return(f"Reservation at {location} has been booked on {date} at time {slot} for {seats_needed} people")
    return (f"Could not make the reservation at {location} since {seats_needed} seats were not available. Ask the user if they want to try another venue.")
    
    




