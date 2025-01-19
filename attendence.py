############################################# IMPORTING ################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2, os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time

############################################# FUNCTIONS ################################################

def assure_path_exists(path):
    """Ensure a directory exists; create if not."""
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

##################################################################################

def tick():
    """Update the clock label every 200ms."""
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200, tick)

###################################################################################

def contact():
    """Display contact info in a message box."""
    mess._show(title='Contact us', message="Please contact us on : 'xxxxxxxxxxxxx@gmail.com' ")

###################################################################################

def check_haarcascadefile():
    """Check if Haar Cascade file exists. If missing, prompt error."""
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if not exists:
        mess._show(title='Some file missing', message='Please contact us for help')
        window.destroy()

###################################################################################

def save_pass():
    """Save or change the password for image training."""
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\\psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas is None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
        return

    op = old.get()
    newp = new.get()
    nnewp = nnew.get()
    if op == key:
        if newp == nnewp:
            txf = open("TrainingImageLabel\\psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
            return
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')
        return

    mess._show(title='Password Changed', message='Password changed successfully!!')
    master.destroy()

###################################################################################

def change_pass():
    """Open a small window to change the training password."""
    global master
    master = tk.Tk()
    master.geometry("400x200")
    master.resizable(False, False)
    master.title("Change Password")
    master.configure(background="#2d3436")

    # Labels
    lbl4 = tk.Label(master, text='Enter Old Password', bg='#2d3436', fg='white', font=('Helvetica', 12, 'bold'))
    lbl4.place(x=30, y=20)

    lbl5 = tk.Label(master, text='Enter New Password', bg='#2d3436', fg='white', font=('Helvetica', 12, 'bold'))
    lbl5.place(x=30, y=70)

    lbl6 = tk.Label(master, text='Confirm New Password', bg='#2d3436', fg='white', font=('Helvetica', 12, 'bold'))
    lbl6.place(x=30, y=120)

    # Entries
    global old, new, nnew
    old = tk.Entry(master, width=25, fg="black", relief='solid', font=('Helvetica', 12, 'bold'), show='*')
    old.place(x=200, y=20)

    new = tk.Entry(master, width=25, fg="black", relief='solid', font=('Helvetica', 12, 'bold'), show='*')
    new.place(x=200, y=70)

    nnew = tk.Entry(master, width=25, fg="black", relief='solid', font=('Helvetica', 12, 'bold'), show='*')
    nnew.place(x=200, y=120)

    # Buttons
    save1 = tk.Button(master, text="Save", command=save_pass,
                      fg="white", bg="#00b894", width=8, activebackground="#55efc4",
                      font=('Helvetica', 10, 'bold'))
    save1.place(x=80, y=160)

    cancel = tk.Button(master, text="Cancel", command=master.destroy,
                       fg="white", bg="#d63031", width=8, activebackground="#ff7675",
                       font=('Helvetica', 10, 'bold'))
    cancel.place(x=220, y=160)

    master.mainloop()

#####################################################################################

def psw():
    """Check password before training images."""
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\\psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas is None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
        return

    password = tsd.askstring('Password', 'Enter Password', show='*')
    if password == key:
        TrainImages()
    elif password is None:
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')

######################################################################################

def clear():
    """Clear the ID entry field."""
    txt.delete(0, 'end')
    message1.configure(text="1)Take Images  >>>  2)Save Profile")

def clear2():
    """Clear the Name entry field."""
    txt2.delete(0, 'end')
    message1.configure(text="1)Take Images  >>>  2)Save Profile")

#######################################################################################

def TakeImages():
    """Capture and save images for a new registration."""
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
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
            writer.writerow(columns)
            serial = 1
        csvFile1.close()

    Id = txt.get()
    name = txt2.get()

    if (name.isalpha()) or (' ' in name):
        cam = cv2.VideoCapture(0)
        detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        sampleNum = 0

        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sampleNum += 1
                cv2.imwrite(f"TrainingImage\\{name}.{serial}.{Id}.{sampleNum}.jpg", gray[y:y + h, x:x + w])
                cv2.imshow('Taking Images', img)

            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sampleNum > 100:
                break

        cam.release()
        cv2.destroyAllWindows()

        res = "Images Taken for ID : " + Id
        row = [serial, '', Id, '', name]
        with open(csv_path, 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message1.configure(text=res)
    else:
        if not name.isalpha():
            message.configure(text="Enter Correct name")

########################################################################################

def TrainImages():
    """Train the saved images to create or update the face recognition model."""
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return

    recognizer.save("TrainingImageLabel\\Trainner.yml")
    res = "Profile Saved Successfully"
    message1.configure(text=res)
    message.configure(text='Total Registrations till now  : ' + str(ID[0]))

############################################################################################

def getImagesAndLabels(path):
    """Return face samples and IDs from the training images."""
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []

    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(ID)

    return faces, Ids

###########################################################################################

import pandas as pd

def TrackImages():
    """Detect and record attendance using the trained face recognizer."""
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")

    # Clear the treeview first
    for k in tv.get_children():
        tv.delete(k)

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    exists3 = os.path.isfile("TrainingImageLabel\\Trainner.yml")
    if not exists3:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    recognizer.read("TrainingImageLabel\\Trainner.yml")

    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Name', 'Date', 'Time']

    csv_path = "StudentDetails\\StudentDetails.csv"
    if os.path.isfile(csv_path):
        df = pd.read_csv(csv_path)
    else:
        mess._show(title='Details Missing', message='Students details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()

    attendance_record = None
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if conf < 50:
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

                # Find name & ID from CSV
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID_val = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID_str = str(ID_val)[1:-1]
                name_str = str(aa)[2:-2]

                attendance_record = [ID_str, name_str, date, timeStamp]
                cv2.putText(im, name_str, (x, y + h), font, 1, (255, 255, 255), 2)
            else:
                cv2.putText(im, 'Unknown', (x, y + h), font, 1, (255, 255, 255), 2)

        cv2.imshow('Taking Attendance', im)
        if cv2.waitKey(1) == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

    # Save the attendance record to an Excel file
    if attendance_record:
        date = attendance_record[2]
        attend_excel = f"Attendance\\Attendance_{date}.xlsx"
        
        # Check if the Excel file already exists
        if os.path.isfile(attend_excel):
            # Load the existing Excel file
            df_existing = pd.read_excel(attend_excel)
            # Append the new record
            df_new = pd.DataFrame([attendance_record], columns=col_names)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined.to_excel(attend_excel, index=False)
        else:
            # Create a new Excel file with the attendance record
            df_new = pd.DataFrame([attendance_record], columns=col_names)
            df_new.to_excel(attend_excel, index=False)

        # Display in treeview
        i = 0
        with open(attend_excel, 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for lines in reader1:
                i += 1
                if (i > 1) and (i % 2 != 0):
                    iidd = str(lines[0]) + '   '
                    tv.insert('', 0, text=iidd, values=(lines[1], lines[2], lines[3]))


######################################## USED STUFFS ############################################

global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day, month, year = date.split("-")

mont = {
    '01': 'January', '02': 'February', '03': 'March', '04': 'April',
    '05': 'May', '06': 'June',     '07': 'July',     '08': 'August',
    '09': 'September','10': 'October','11': 'November','12': 'December'
}

######################################## GUI FRONT-END ###########################################

window = tk.Tk()
window.title("Attendance System - Dark Mode")
window.geometry("1280x720")
window.resizable(True, False)

# Optional icon
# window.iconbitmap("icon.ico")

# --------------------- DARK BACKGROUND + FRAMES ---------------------

window.configure(bg="#1e272e")  # Dark background

# Main title label across top
title_label = tk.Label(
    window,
    text="Face Recognition Based Attendance System",
    bg="#2f3640",      # Dark bar
    fg="#f5f6fa",
    font=("Helvetica", 26, "bold"),
    relief='ridge'
)
title_label.place(x=0, y=0, relwidth=1, height=60)

# Date & Time Frame
top_frame = tk.Frame(window, bg="#2f3640")
top_frame.place(x=0, y=60, relwidth=1, height=50)

date_text = f"{day}-{mont[month]}-{year}  |  "
date_label = tk.Label(
    top_frame,
    text=date_text,
    bg="#2f3640",
    fg="#f5f6fa",
    font=("Helvetica", 16, "bold")
)
date_label.pack(side="left", padx=15)

clock = tk.Label(top_frame, bg="#2f3640", fg="#f5f6fa", font=("Helvetica", 16, "bold"))
clock.pack(side="right", padx=15)
tick()  # Start updating time

# Left Frame (Attendance + Quit)
frame1 = tk.Frame(window, bg="#2d3436", bd=2, relief="ridge")
frame1.place(x=20, y=120, width=500, height=570)

head1 = tk.Label(
    frame1,
    text="For Already Registered",
    fg="white", bg="#3d3d3d",
    font=("Helvetica", 18, "bold")
)
head1.pack(fill="x")

trackImg = tk.Button(
    frame1,
    text="Take Attendance",
    command=TrackImages,
    fg="white",
    bg="#0984e3",
    activebackground="#74b9ff",
    font=("Helvetica", 15, "bold"),
    width=20
)
trackImg.place(x=140, y=60)

quitWindow = tk.Button(
    frame1,
    text="Quit",
    command=window.destroy,
    fg="white",
    bg="#e74c3c",
    activebackground="#ff7675",
    font=("Helvetica", 15, "bold"),
    width=20
)
quitWindow.place(x=140, y=500)

lbl3 = tk.Label(
    frame1,
    text="Attendance",
    fg="#dfe6e9",
    bg="#2d3436",
    font=("Helvetica", 16, "bold")
)
lbl3.place(x=190, y=130)

tv = ttk.Treeview(frame1, height=8, columns=('name','date','time'))
tv.column('#0', width=70)
tv.column('name', width=120)
tv.column('date', width=120)
tv.column('time', width=120)
tv.place(x=30, y=170)
tv.heading('#0', text='ID')
tv.heading('name', text='NAME')
tv.heading('date', text='DATE')
tv.heading('time', text='TIME')

scroll = ttk.Scrollbar(frame1, orient='vertical', command=tv.yview)
scroll.place(x=470, y=170, height=177)
tv.configure(yscrollcommand=scroll.set)

# Right Frame (New Registrations)
frame2 = tk.Frame(window, bg="#2d3436", bd=2, relief="ridge")
frame2.place(x=540, y=120, width=720-40, height=570)

head2 = tk.Label(
    frame2,
    text="For New Registrations",
    fg="white",
    bg="#3d3d3d",
    font=("Helvetica", 18, "bold")
)
head2.pack(fill="x")

# ID
lbl = tk.Label(frame2, text="Enter ID", fg="white", bg="#2d3436", font=("Helvetica", 15, "bold"))
lbl.place(x=80, y=60)

txt = tk.Entry(frame2, width=30, fg="#000", font=("Helvetica", 13, "bold"))
txt.place(x=80, y=100)

# Name
lbl2 = tk.Label(frame2, text="Enter Name", fg="white", bg="#2d3436", font=("Helvetica", 15, "bold"))
lbl2.place(x=80, y=150)

txt2 = tk.Entry(frame2, width=30, fg="#000", font=("Helvetica", 13, "bold"))
txt2.place(x=80, y=190)

message1 = tk.Label(frame2, text="1)Take Images  >>>  2)Save Profile",
                    bg="#2d3436", fg="#dfe6e9",
                    font=("Helvetica", 13, "bold"))
message1.place(x=80, y=240)

message = tk.Label(frame2, text="", bg="#2d3436", fg="#dfe6e9", font=("Helvetica", 13, "bold"))
message.place(x=80, y=470)

# Buttons
clearButton = tk.Button(
    frame2,
    text="Clear ID",
    command=clear,
    fg="white",
    bg="#e74c3c",
    activebackground="#ff7675",
    font=("Helvetica", 11, "bold"),
    width=10
)
clearButton.place(x=360, y=98)

clearButton2 = tk.Button(
    frame2,
    text="Clear Name",
    command=clear2,
    fg="white",
    bg="#e74c3c",
    activebackground="#ff7675",
    font=("Helvetica", 11, "bold"),
    width=10
)
clearButton2.place(x=360, y=188)

takeImg = tk.Button(
    frame2,
    text="Take Images",
    command=TakeImages,
    fg="white",
    bg="#00cec9",
    activebackground="#81ecec",
    font=("Helvetica", 15, "bold"),
    width=14
)
takeImg.place(x=80, y=300)

trainImg = tk.Button(
    frame2,
    text="Save Profile",
    command=psw,
    fg="white",
    bg="#00cec9",
    activebackground="#81ecec",
    font=("Helvetica", 15, "bold"),
    width=14
)
trainImg.place(x=280, y=300)

# Menubar
menubar = tk.Menu(window, relief='ridge')
filemenu = tk.Menu(menubar, tearoff=0, bg="#2d3436", fg="white", activebackground="#0984e3")
filemenu.add_command(label='Change Password', command=change_pass)
filemenu.add_command(label='Contact Us', command=contact)
filemenu.add_command(label='Exit', command=window.destroy)
menubar.add_cascade(label='Help', font=('Helvetica', 12, 'bold'), menu=filemenu)
window.configure(menu=menubar)

# Check existing registrations
res = 0
details_csv = "StudentDetails\\StudentDetails.csv"
if os.path.isfile(details_csv):
    with open(details_csv, 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for _ in reader1:
            res += 1
    csvFile1.close()
    # Each entry is 2 lines in the CSV, minus 1 for header
    res = (res // 2) - 1
message.configure(text='Total Registrations till now  : ' + str(max(res, 0)))

window.mainloop()
