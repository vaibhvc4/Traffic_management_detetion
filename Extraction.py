import cv2
import pytesseract
import re
import numpy as np
import matplotlib.pyplot as plt
from Api_ocr import fun
import mysql.connector
import datetime
from API import database
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
config = {
    "host": "localhost",
    "user": "vaibhav",
    "password": "vaibhav@123__",
    "database": "vaibhav",
    'auth_plugin':'mysql_native_password'
}
# connection = mysql.connector.connect(**config)

curr_time =str(datetime.datetime.now())


def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 30, 150)
    return img, gray, edged

def find_license_plate(edged):
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    location = None

    for contour in contours:
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) == 4:
            location = approx
            break

    return location

def extract_license_plate(img, location):
    if location is None:
        return None

    polygon_corners = location.reshape(-1, 2)
    (x_poly, y_poly) = polygon_corners.min(axis=0)
    (x1_poly, y1_poly) = polygon_corners.max(axis=0)
    cropped_polygon = img[y_poly:y1_poly + 2, x_poly:x1_poly + 2]
    return cropped_polygon

def ocr_license_plate(cropped_polygon):
    text_polygon = pytesseract.image_to_string(
        cropped_polygon,
        lang='eng',
        config='--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.'
    )
    filtered_text = re.sub(r'[^A-Z\d.\s\n-]', '', text_polygon)
    return filtered_text

def main(image_path, output_path):
    img, gray, edged = preprocess_image(image_path)
    location = find_license_plate(edged)
    cropped_polygon = extract_license_plate(gray, location)

    if cropped_polygon is not None and isinstance(cropped_polygon, np.ndarray):
        cv2.imwrite(output_path, cropped_polygon)

        plt.figure(figsize=(8, 4))
        plt.imshow(cropped_polygon, cmap='gray')
        plt.title("Cropped License Plate")
        plt.axis('off')
        plt.show()

        result = ocr_license_plate(cropped_polygon)
        return result
    else:
        print("Error: Cropped image is not a valid NumPy array or license plate not found.")
        return None

def start(img_path):
    global curr_time
    image_path = img_path
    output_path = r"D:\weights_hel_bike\output_path\img.png"
    license_plate_text = main(image_path, output_path)
    if license_plate_text:
        print("License Plate Text:", license_plate_text)
        # fun()
    else:
        print("OCR processing failed.")
    
    # if connection.is_connected():
    #         print("Connected to MySQL database")

    #         # Create a cursor object to interact with the database
    #         cursor = connection.cursor()

    #         # Execute SQL queries
    #         cursor.execute(f"INSERT INTO driver(number_plate, dates, helmet_on) values('{license_plate_text}','{curr_time}',1)")
    #         cursor.execute(f'SELECT * FROM driver')

            
    #         results = cursor.fetchall()
    #         for row in results:
    #                     # Access columns by index or name
    #             column1 = row[0]
    #             column2 = row[1]
    #             column3 = row[2]
    #             column4= row[3]
    #         print(column1)
    #         print(column2)
    #         print(column3)
    #         print(column4)
    #         connection.commit()
    database(license_plate_text)
    

# start(r'D:\react_sql\bra_on.png')