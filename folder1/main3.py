import customtkinter as ctk
from tkinter import ttk  # Import ttk for Treeview
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2, os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time

############################################## Functions ###############################

def on_enter(event):
    message1.configure(bg_color="#3ffc00")  # Change to hover color

def on_leave(event):
    message1.configure(bg_color="#c79cff")  # Revert to original color

def assure_path_exists(path):
    dir = os.path.dirname(path)  # Check if the directory exists
    if not os.path.exists(dir):
        os.makedirs(dir)  # Create the directory if it doesn't exist
        
def tick():
    time_string = time.strftime('%H:%M:%S')
    clock_label.configure(text=time_string)
    clock_label.after(200, tick)  # Update data after every 200 milliseconds

def contact():
    mess._show(title='Contact us', message="Please contact us on: 'reekparnasen@gmail.com'")

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")  # Check for the haarcascade file
    if not exists:
        mess._show(title='Some file missing', message="Please contact us for help.")
        window.destroy()

def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel/password.txt")
    if exists1:
        with open("TrainingImageLabel/password.txt", "r") as tf:
            key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show="*")
        if new_pas is None:
            mess._show(title='No Password Entered', message='Password not set! Please try again')
        else:
            with open("TrainingImageLabel/password.txt", "w") as tf:
                tf.write(new_pas)
            mess._show(title='Password registered', message='New Password was registered successfully!')
            return

    op = old.get()
    newp = new.get()
    nnewp = nnew.get()
    if op == key:
        if newp == nnewp:
            with open("TrainingImageLabel/password.txt", "w") as txf:
                txf.write(newp)
        else:
            mess._show(title='Error', message="Confirm new password again!")
            return
    else:
        mess._show(title='Wrong Password', message='Please enter the correct old password.')
        return
    mess._show(title='Password changed', message='Password changed successfully!')
    master.destroy()

def change_pass():
    global master
    master = ctk.CTk()
    master.geometry("400x160")
    master.resizable(False, False)
    master.title("Change Password")
    master.configure(fg_color="white")

    lbl4 = ctk.CTkLabel(master, text='Enter Old Password', fg_color='white', text_color='black', font=('comic', 12, 'bold'))
    lbl4.place(x=10, y=10)

    global old
    old = ctk.CTkEntry(master, width=180, fg_color="white", text_color="black", font=('comic', 12, 'bold'), show='*', border_width=1)
    old.place(x=180, y=10)

    lbl5 = ctk.CTkLabel(master, text='Enter New Password', fg_color='white', text_color='black', font=('comic', 12, 'bold'))
    lbl5.place(x=10, y=45)

    global new
    new = ctk.CTkEntry(master, width=180, fg_color="white", text_color="black", font=('comic', 12, 'bold'), show='*', border_width=1)
    new.place(x=180, y=45)

    lbl6 = ctk.CTkLabel(master, text='Confirm New Password', fg_color='white', text_color='black', font=('comic', 12, 'bold'))
    lbl6.place(x=10, y=80)

    global nnew
    nnew = ctk.CTkEntry(master, width=180, fg_color="white", text_color="black", font=('comic', 12, 'bold'), show='*', border_width=1)
    nnew.place(x=180, y=80)

    cancel = ctk.CTkButton(master, text="Cancel", command=master.destroy, fg_color="red", text_color="black", font=('comic', 10, 'bold'))
    cancel.place(x=200, y=120)

    save1 = ctk.CTkButton(master, text="Save", command=save_pass, fg_color="#00fcca", text_color="black", font=('comic', 10, 'bold'))
    save1.place(x=10, y=120)

    master.mainloop()

def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel/password.txt")
    if exists1:
        with open("TrainingImageLabel/password.txt", "r") as tf:
            key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below.', show="*")
        if new_pas is None:
            mess._show(title='No Password Entered', message='Password not set! Please try again')
        else:
            with open("TrainingImageLabel/password.txt", "w") as tf:
                tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if password == key:
        TrainImage()
    elif password is None:
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered the wrong password')

def clear():
    txt.delete(0, 'end')
    message1.configure(text="1) Take Images  >>>  2) Save Profile")

def clear2():
    txt2.delete(0, 'end')
    message1.configure(text="1) Take Images  >>>  2) Save Profile")

def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', 'ID', 'NAME']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImages/")
    serial = 1
    exists = os.path.isfile("StudentDetails/StudentDetails.csv")
    if exists:
        with open("StudentDetails/StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for _ in reader1:
                serial += 1
        serial = (serial // 2)
    else:
        with open("StudentDetails/StudentDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1

    Id = txt.get()
    name = txt2.get()
    if name.isalpha() or ' ' in name:
        cam = cv2.VideoCapture(0)
        haarcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(haarcascadePath)
        sampleNum = 0
        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sampleNum += 1
                cv2.imwrite("TrainingImages/" + name + "." + str(serial) + "." + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
            cv2.imshow('Taking Images', img)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Taken for ID : " + Id
        row = [serial, '', Id, '', name]
        with open('StudentDetails/StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        message1.configure(text=res)
    else:
        message1.configure(text="Enter Correct Name")

def TrainImage():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    haarcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(haarcascadePath)
    faces, Ids = getImagesAndLabels("TrainingImages/")
    try:
        recognizer.train(faces, np.array(Ids))
    except:
        mess._show(title='No Registrations', message='Please register someone first!')
        return
    recognizer.save("TrainingImageLabel/Trainner.yml")
    res = "Profile Saved Successfully"
    message1.configure(text=res)
    message1.configure(text="All Profiles Saved Successfully")

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids

def TrackImages():
    # Load the CSV file
    df = pd.read_csv(r"D://Projects//python-ai-ml-projects//face-reco//StudentDetails//StudentDetails.csv")

    # Print the current columns to debug
    print("Columns in the DataFrame:", df.columns)

    # Rename the columns to match your data structure
    df.columns = ['SERIAL NO.', 'ID', 'NAME']  # Adjust based on your actual data

    # Verify the renaming
    print("Renamed Columns:", df.columns)

    # Continue with your existing logic
    Id = 'some_id'  # Replace with actual logic to get the Id
    try:
        aa = df.loc[df['Id'] == Id]['Name'].values
        print(aa)  # Debugging: Print the result to ensure it's correct
    except KeyError as e:
        print(f"KeyError: {e} - Column not found in DataFrame")
        
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")
    for k in tv.get_children():
        tv.delete(k)
    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    exists3 = os.path.isfile("TrainingImageLabel/Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel/Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    haarcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(haarcascadePath)

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    exists1 = os.path.isfile("StudentDetails/StudentDetails.csv")
    if exists1:
        df = pd.read_csv("StudentDetails/StudentDetails.csv")
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]  # Remove 'Unnamed' columns
        print(df.columns)  # Debug line to check column names
    else:
        mess._show(title='Details Missing', message='Students details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
    
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if conf < 50:
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['Id'] == Id]['Name'].values  # Replace with correct column name
                tt = str(Id) + "-" + str(aa)
                attendance = [str(Id), '', aa, '', date, '', timeStamp]
                tv.insert('', 0, text=tt, values=attendance)
            else:
                Id = 'Unknown'
                tt = str(Id)
            if conf > 75:
                noOfFile = len(os.listdir("ImagesUnknown")) + 1
                cv2.imwrite("ImagesUnknown/Image" + str(noOfFile) + ".jpg", im[y:y + h, x:x + w])
            cv2.putText(im, str(tt), (x, y + h), font, 1, (255, 255, 255), 2)
        cv2.imshow('Tracking', im)
        if cv2.waitKey(1) == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()

    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour, Minute, Second = timeStamp.split(":")
    fileName = "Attendance/Attendance_" + date + "_" + Hour + "-" + Minute + "-" + Second + ".csv"
    with open(fileName, 'a+') as csvFile1:
        writer = csv.writer(csvFile1)
        writer.writerow(col_names)
        for k in tv.get_children():
            writer.writerow(tv.item(k)['values'])
    res = tv.get_children()
    for i in res:
        tv.delete(i)



def update_clock():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    clock_label.configure(text=now)
    clock_label.after(1000, update_clock)

######################################## Main GUI #######################################

window = ctk.CTk()  # Initialize the window
window.geometry("1024x768")  # Set window size
window.title("Face Recognition Attendance System")

# Clock Display
clock_label = ctk.CTkLabel(window, text="", font=("Helvetica", 20))
clock_label.place(x=20, y=20)
update_clock()


# Title
message1 = ctk.CTkLabel(window, text="Face Recognition Attendance System", font=("Arial", 35, 'bold'), text_color="#c79cff")
message1.place(x=250, y=20)

# Labels and Entry Fields
lbl = ctk.CTkLabel(window, text="Enter ID", font=("Arial", 20))
lbl.place(x=50, y=200)

txt = ctk.CTkEntry(window, font=("Arial", 20), border_width=1, fg_color='black', width=300, height=40)
txt.place(x=300, y=200)

lbl2 = ctk.CTkLabel(window, text="Enter Name", font=("Arial", 20))
lbl2.place(x=50, y=250)

txt2 = ctk.CTkEntry(window, font=("Arial", 20), border_width=1, fg_color='black',  width=300, height=40)
txt2.place(x=300, y=250)

# Buttons
takeImg = ctk.CTkButton(window, text="Take Images", command=TakeImages, fg_color="#00fcca", text_color="black", font=("Arial", 18, 'bold'), width=200, height=50)
takeImg.place(x=650, y=200)

trainImg = ctk.CTkButton(window, text="Save Profile", command=psw, fg_color="#00fcca", text_color="black", font=("Arial", 18, 'bold'), width=200, height=50)
trainImg.place(x=650, y=300)

trackImg = ctk.CTkButton(window, text="Take Attendance", command=TrackImages, fg_color="#00fcca", text_color="black", font=("Arial", 18, 'bold'), width=200, height=50)
trackImg.place(x=650, y=400)

quitWindow = ctk.CTkButton(window, text="Quit", command=window.destroy, fg_color="red", text_color="black", font=("Arial", 18, 'bold'), width=200, height=50)
quitWindow.place(x=650, y=500)

clearButton = ctk.CTkButton(window, text="Clear", command=clear, fg_color="red", text_color="black", font=("Arial", 18, 'bold'), width=150, height=50)
clearButton.place(x=950, y=200)

clearButton2 = ctk.CTkButton(window, text="Clear", command=clear2, fg_color="red", text_color="black", font=("Arial", 18, 'bold'), width=150, height=50)
clearButton2.place(x=950, y=300)

# Attendance Table
tv = ttk.Treeview(window, height=15, columns=("Serial", "ID", "Name", "Date", "Time"))
tv.column("Serial", width=100)
tv.column("ID", width=100)
tv.column("Name", width=200)
tv.column("Date", width=150)
tv.column("Time", width=150)
tv.place(x=50, y=450)

tv.heading("Serial", text="Serial No.")
tv.heading("ID", text="ID")
tv.heading("Name", text="Name")
tv.heading("Date", text="Date")
tv.heading("Time", text="Time")

# Main Loop
window.mainloop()
