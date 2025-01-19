from flask import Flask, render_template, request, redirect, url_for, flash
import cv2
import os
import pandas as pd
import datetime
import csv

app = Flask(__name__)
app.secret_key = "your_secret_key"  # For flashing messages

# Ensure required directories exist
def assure_path_exists(path):
    """Ensure a directory exists; create if not."""
    if not os.path.exists(path):
        os.makedirs(path)

# Upload Haar Cascade file for face detection
def check_haarcascadefile():
    """Check if Haar Cascade file exists. If missing, prompt error."""
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if not exists:
        flash('Haar Cascade XML file is missing, please upload it.', 'error')
        return False
    return True

# Register student and capture images
def take_images(Id, name):
    if not check_haarcascadefile():
        return

    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")

    serial = 0
    csv_path = "StudentDetails\\StudentDetails.csv"
    exists = os.path.isfile(csv_path)
    
    if exists:
        with open(csv_path, 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for _ in reader1:
                serial += 1
        serial = serial // 2
        csvFile1.close()
    else:
        with open(csv_path, 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(['SERIAL NO.', 'ID', 'NAME'])
            serial = 1
        csvFile1.close()

    # Initialize camera
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        flash('Error: Could not access the camera!', 'error')
        return

    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    sampleNum = 0

    while True:
        ret, img = cam.read()

        if not ret:
            #flash('Error: Failed to capture image!', 'error')
            break

        # Convert the captured image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = detector.detectMultiScale(gray, 1.3, 5)

        # If no faces detected, notify the user
        if len(faces) == 0:
            flash('No face detected! Please position your face properly.', 'error')

        # Process detected faces
        for (x, y, w, h) in faces:
            sampleNum += 1
            cv2.imwrite(f"TrainingImage\\{name}.{serial}.{Id}.{sampleNum}.jpg", gray[y:y + h, x:x + w])

        # Stop after capturing 100 samples
        if sampleNum >= 100:
            flash(f"Successfully captured {sampleNum} images!", 'success')
            break

    # Release the camera after capturing images
    cam.release()

    # Save registration details to CSV
    row = [serial, Id, name]
    with open(csv_path, 'a+') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    
    # Optionally, you can return a confirmation or redirect message

# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        Id = request.form['id']
        name = request.form['name']
        take_images(Id, name)
        flash(f"Images taken and saved for ID: {Id}", 'success')
        return redirect(url_for('index'))
    
    

if __name__ == "__main__":
    app.run(debug=True)
