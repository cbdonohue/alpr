import cv2
import openalpr
import shutil
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                    handlers=[logging.StreamHandler()])

def preprocess_image(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to the image
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply adaptive threshold to the image
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Save the preprocessed image
    cv2.imwrite(image_path, thresh)
    

def copy_image(src_file, dst_file):
    shutil.copy(src_file, dst_file)
    logging.info(f"Image file copied from {src_file} to {dst_file}")

def capture_frame(url):
    cap = cv2.VideoCapture(url)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite('frame.jpg', frame)
        logging.info('Captured frame successfully')
    else:
        logging.error('Failed to capture frame')

def recognize_plate(image_path, region='us'):
    # Initialize the OpenALPR library
    alpr = openalpr.Alpr(region, "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")

    # Read the license plate numbers from the image
    results = alpr.recognize_file(image_path)

    # Iterate through the results and log the license plate numbers
    for plate in results["results"]:
        logging.info("Plate: " + plate["plate"])
        logging.info("Confidence: " + str(plate["confidence"]))

        if plate["confidence"] > 80:
            copy_image(image_path, plate['plate'] + '.jpg')

    # Unload the OpenALPR library
    alpr.unload()

if __name__ == '__main__':
    while True:
        capture_frame('rtsp://192.168.1.202:554/11')
        preprocess_image('frame.jpg')
        recognize_plate("frame.jpg")
