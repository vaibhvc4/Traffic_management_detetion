
import mysql.connector
from datetime import datetime
# from Detection import helmet_detected
# Create a MySQL connection
def database(plate):
    
    
    vehicle_no =plate.strip()
    helmet_status = 0
    config = {
        "host": "localhost",
        "user": "vaibhav",
        "password": "vaibhav@123__",
        "database": "vaibhav2",
        'auth_plugin':'mysql_native_password'
    }
    conn =mysql.connector.connect(**config)

    cursor = conn.cursor()

    print(conn)

    place = "Surathkal"
    new_time = str(datetime.now())  

    insert_driver_query = """
        INSERT INTO drivers (vehicle_no, place, time)
        VALUES (%s, %s, %s)
    """
    cursor.execute(insert_driver_query, (vehicle_no, place, new_time))
    conn.commit()


    fetch_latest_entries_query = """
        CREATE TEMPORARY TABLE temp_latest_entries AS
        SELECT MAX(id) AS latest_id, vehicle_no
        FROM drivers
        GROUP BY vehicle_no
    """

    cursor.execute(fetch_latest_entries_query)


    delete_duplicates_query = """
        DELETE FROM drivers
        WHERE id NOT IN (SELECT latest_id FROM temp_latest_entries)
    """

    cursor.execute(delete_duplicates_query)


    conn.commit()
    # Close the cursor and database connection when done
    vehicle_id_mapping = {}

    # Fetch id from drivers based on vehicle_no
    select_driver_id_query = "SELECT id, vehicle_no FROM drivers"
    cursor.execute(select_driver_id_query)
    driver_data = cursor.fetchall()

    for row in driver_data:
        driver_id, vehicle_no = row
        vehicle_id_mapping[vehicle_no] = driver_id
    print(vehicle_id_mapping)




    current_date = datetime.now().date()

    select_expired_insurance_query = "SELECT vehicle_no, owner FROM rto_details WHERE insurance_validity <= %s;"
    cursor.execute(select_expired_insurance_query, (current_date,))
    expired_insurance_data = cursor.fetchall()

    select_expired_emission_query = "SELECT vehicle_no, owner FROM rto_details WHERE emission_validity <= %s;"
    cursor.execute(select_expired_emission_query, (current_date,))
    expired_emission_data = cursor.fetchall()


    select_expired_both_query = "SELECT vehicle_no, owner FROM rto_details WHERE insurance_validity <= %s AND emission_validity <= %s;"
    cursor.execute(select_expired_both_query, (current_date, current_date))
    expired_both_data = cursor.fetchall()


    select_expired_none = "SELECT vehicle_no, owner FROM rto_details WHERE insurance_validity >= %s AND emission_validity >= %s;"
    cursor.execute(select_expired_none, (current_date, current_date))
    expired_None = cursor.fetchall()


    for row in expired_insurance_data:
        vehicle_no, owner = row
        if vehicle_no in vehicle_id_mapping:
            driver_id = vehicle_id_mapping[vehicle_no]
            violation_id = str(helmet_status) + '1' + '0'  # Helmet violation only
            check_existing_query = "SELECT COUNT(*) FROM violations WHERE notice_id = %s;"
            cursor.execute(check_existing_query, (driver_id,))
            existing_count = cursor.fetchone()[0]
        

            if existing_count == 0:
                insert_owner_query = "INSERT INTO violations (notice_id, vehicle_no, helmet_status, insurance_status, emission_status, violation_id) VALUES (%s, %s, %s, %s, %s, %s);"
                cursor.execute(insert_owner_query, (driver_id, vehicle_no, helmet_status, 1, 0, int(violation_id)))

    for row in expired_emission_data:
        vehicle_no, owner = row
        if vehicle_no in vehicle_id_mapping:
            driver_id = vehicle_id_mapping[vehicle_no]
            violation_id = str(helmet_status) + '0' + '1'  # Helmet violation only
            check_existing_query = "SELECT COUNT(*) FROM violations WHERE notice_id = %s;"
            cursor.execute(check_existing_query, (driver_id,))
            existing_count = cursor.fetchone()[0]

            if existing_count == 0:
                insert_owner_query = "INSERT INTO violations (notice_id, vehicle_no, helmet_status, insurance_status, emission_status, violation_id) VALUES (%s, %s, %s, %s, %s, %s);"
                cursor.execute(insert_owner_query, (driver_id, vehicle_no, helmet_status, 0, 1, int(violation_id)))
        

    for row in expired_both_data:
        vehicle_no, owner = row
        if vehicle_no in vehicle_id_mapping:
            driver_id = vehicle_id_mapping[vehicle_no]
            violation_id = str(helmet_status) + '1' + '1'  
            check_existing_query = "SELECT COUNT(*) FROM violations WHERE notice_id = %s;"
            cursor.execute(check_existing_query, (driver_id,))
            existing_count = cursor.fetchone()[0]

            if existing_count == 0:
                insert_owner_query = "INSERT INTO violations (notice_id, vehicle_no, helmet_status, insurance_status, emission_status, violation_id) VALUES (%s, %s, %s, %s, %s, %s);"
                cursor.execute(insert_owner_query, (driver_id, vehicle_no, helmet_status, 1, 1, int(violation_id)))

    for row in expired_None:
        vehicle_no, owner = row
        if vehicle_no in vehicle_id_mapping and helmet_status == 1:
            driver_id = vehicle_id_mapping[vehicle_no]
            violation_id = str(helmet_status) + '0' + '0'  
            check_existing_query = "SELECT COUNT(*) FROM violations WHERE notice_id = %s;"
            cursor.execute(check_existing_query, (driver_id,))
            existing_count = cursor.fetchone()[0]

            if existing_count == 0:
                insert_owner_query = "INSERT INTO violations (notice_id, vehicle_no, helmet_status, insurance_status, emission_status, violation_id) VALUES (%s, %s, %s, %s, %s, %s);"
                cursor.execute(insert_owner_query, (driver_id, vehicle_no, helmet_status, 0, 0, int(violation_id)))

    fetch_latest_entries_query = """
        CREATE TEMPORARY TABLE temp1_latest_entries AS
        SELECT MAX(notice_id) AS latest_id, vehicle_no
        FROM violations
        GROUP BY vehicle_no
    """

    cursor.execute(fetch_latest_entries_query)


    delete_duplicates_query = """
        DELETE FROM violations
        WHERE notice_id NOT IN (SELECT latest_id FROM temp1_latest_entries)
    """

    cursor.execute(delete_duplicates_query)

    conn.commit()



    select_violations_query = "SELECT notice_id, vehicle_no, helmet_status, insurance_status, emission_status FROM violations;"
    cursor.execute(select_violations_query)
    violations_data = cursor.fetchall()

    for row in violations_data:
        notice_id, vehicle_no, helmet_status, insurance_status, emission_status = row

        # Check if any violation is detected
        if helmet_status == 1 or insurance_status == 1 or emission_status == 1:
            # Calculate fines based on violation flags
            helmet_fine = 1000 if helmet_status == 1 else 0
            insurance_fine = 1000 if insurance_status == 1 else 0
            emission_fine = 1000 if emission_status == 1 else 0

            # Calculate total fine
            total_fine = helmet_fine + insurance_fine + emission_fine

            # Insert payment record
            insert_payment_query = """
                INSERT INTO payments (notice_id, vehicle_no, helmet_fine, insurance_fine, emission_fine, total_fine, payment_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_payment_query, (notice_id, vehicle_no, helmet_fine, insurance_fine, emission_fine, total_fine, current_date))

    fetch_latest_entries_query = """
        CREATE TEMPORARY TABLE temp2_latest_entries AS
        SELECT MAX(notice_id) AS latest_id, vehicle_no
        FROM payments
        GROUP BY vehicle_no
    """

    cursor.execute(fetch_latest_entries_query)


    delete_duplicates_query = """
        DELETE p1
        FROM payments p1
        JOIN payments p2 ON p1.notice_id = p2.notice_id AND p1.payment_id > p2.payment_id;
    """
    # cursor.execute(delete_duplicates_query)
    cursor.execute(delete_duplicates_query)

    conn.commit()
