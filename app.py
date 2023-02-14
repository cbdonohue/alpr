import cv2
import queue
import threading
import openalpr
import logging
import shutil
import sqlite3
import numpy as np
from datetime import datetime
import uuid
import os

database_file = "images.db"

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                    handlers=[logging.StreamHandler()])

def add_image_to_database(database_file, image, plate):
    # Convert the image to a binary string
    image_bytes = cv2.imencode('.jpg', image)[1].tobytes()

    # Generate a random UUID
    unique_id = str(uuid.uuid4())

    # Create a filename with the UUID
    filename = f"{plate}_{unique_id}.jpg"

    cv2.imwrite(os.path.join('images', filename), image)

    # Connect to the database
    conn = sqlite3.connect(database_file)
    c = conn.cursor()

    # Create the table if it does not already exist
    c.execute('CREATE TABLE IF NOT EXISTS images (time Text, plate TEXT, filename TEXT)')

    # Insert the image into the database
    time = datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")
    c.execute('INSERT INTO images VALUES (?, ?, ?)', (time, plate, filename))

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

# Set up the video capture from an RTSP stream
rtsp_url = "rtsp://192.168.1.202:554/11"
cap = cv2.VideoCapture(rtsp_url)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# Set up a thread-safe queue to hold the captured frames
frame_queue = queue.Queue(maxsize=20)

# Define a function to capture frames and add them to the queue
def capture_frames():
    global cap

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame from stream")
            cap = cv2.VideoCapture(rtsp_url)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            continue
     
        # Add the current frame to the queue
        try:
            frame_queue.put_nowait(frame)
        except queue.Full:
            pass

        # Wait for one second before capturing the next frame
        cv2.waitKey(1000)

def copy_image(src_file, dst_file):
    shutil.copy(src_file, dst_file)
    logging.info(f"Image file copied from {src_file} to {dst_file}")

def recognize_plate(frame, region='us'):
    # Initialize the OpenALPR library
    alpr = openalpr.Alpr(region, "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")

    # Read the license plate numbers from the image
    ret, enc = cv2.imencode("*.bmp", frame)
    results = alpr.recognize_array(bytes(bytearray(enc)))

    # Iterate through the results and log the license plate numbers
    for plate in results["results"]:
        logging.info("Plate: " + plate["plate"])
        logging.info("Confidence: " + str(plate["confidence"]))

        coordinates = results["results"][0]["coordinates"]
        # Draw a rectangle around the detected license plate
        top_left = (coordinates[0]["x"], coordinates[0]["y"])
        bottom_right = (coordinates[2]["x"], coordinates[2]["y"])
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)

        if plate["confidence"] > 80:
            add_image_to_database(database_file, frame, plate['plate'])

    # Unload the OpenALPR library
    alpr.unload()


# Start a new thread to capture frames and add them to the queue
thread = threading.Thread(target=capture_frames)
thread.daemon = True
thread.start()

# Process frames from the queue
while True:
    # Get the next frame from the queue
    frame = frame_queue.get()

    recognize_plate(frame)

    logging.debug('queue size ' + str(frame_queue.qsize()))

cap.release()
