# Delete certain trip by ID
def deleteTrip(cursor, tripID):
    cursor.execute(f"""
        DELETE FROM SEAT
        WHERE tripID = {tripID};
        DELETE FROM TRIP
        WHERE tripID = {tripID}; """)
    cursor.commit()

# Delete certain train by ID
def deleteTrain(cursor, trainID):
    # Check if Train has no pending trips
    cursor.execute(f"""
        SELECT tripID FROM TRIP
        WHERE trainID = {trainID}
        AND depTime > GETDATE(); """)

    # Check if the customer is already booked on the trip
    if cursor.fetchone() is not None:
        return False

    # If no trips for this train it gets deleted
    cursor.execute(f" DELETE FROM TRAIN WHERE trainID = {trainID}; ")
    cursor.commit()
    return True

# Delete certain user by email
def deleteUser(cursor, email, isAdmin):
    if not isAdmin:
        cursor.execute(f"""
            SELECT customerID FROM SEAT
            WHERE customerID = (
                SELECT customerID FROM CUSTOMER
                WHERE email = '{email}'); """)
        # If the user has trips allocated to him/her cannot delete, return False
        if cursor.fetchone() is not None:
            return False
    # Otherwise, the user is free then delete, return True
    cursor.execute(f" DELETE FROM [USER] WHERE [USER].email = '{email}'; ")
    cursor.commit()
    return True
