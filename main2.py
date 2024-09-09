import customtkinter as ctk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd

import cv2
import os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time


############################################## Functions ###############################

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200, tick)


def contact():
    mess.showinfo(title='Contact us', message="Please contact us on: 'reekparnasen@gmail.com'")


def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if not exists:
        mess.showerror(title='Some file missing', message="Please contact us for help.")
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
            mess.showwarning(title='No Password Entered', message='Password not set! Please try again')
        else:
            with open("TrainingImageLabel/password.txt", "w") as tf:
                tf.write(new_pas)
            mess.showinfo(title='Password registered', message='New Password was registered successfully!')
            return

    op = old.get()
    newp = new.get()
    nnewp = nnew.get()
    if op == key:
        if newp == nnewp:
            with open("TrainingImageLabel/password.txt", "w") as txf:
                txf.write(newp)
        else:
            mess.showerror(title='Error', message="Confirm new password again!")
            return
    else:
        mess.showerror(title='Wrong Password', message='Please enter correct old password.')
        return
    mess.showinfo(title='Password changed', message='Password changed successfully!')
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
            mess.showwarning(title='No Password Entered', message='Password not set! Please try again')
        else:
            with open("TrainingImageLabel/password.txt", "w") as tf:
                tf.write(new_pas)
            mess.showinfo(title='Password Registered', message='New password was registered successfully!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if password == key:
        TrainImage()
    elif password is None:
        pass
    else:
        mess.showerror(title='Wrong Password', message='You have entered wrong password')


def clear():
    txt.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)


def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImages/")
    serial = 0
    exists = os.path.isfile("StudentDetails/StudentDetails.csv")
    if exists:
        with open("StudentDetails/StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
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
                cv2.imwrite(f"TrainingImages/{name}.{serial}.{sampleNum}.jpg", gray[y:y + h, x:x + w])
            cv2.imshow('Taking Images', img)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = f"Images Taken for ID : {Id}"
        row = [serial, '', Id, '', name]
        with open('StudentDetails/StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        message1.configure(text=res)
    else:
        if not name.isalpha():
            res = "Enter Correct Name"
            message.configure(text=res)


def TrainImage():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    haarcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(haarcascadePath)
    faces, ID = getImagesAndLabels("TrainingImages/")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess.showerror(title='No Registrations', message='Please Register someone first!')
        return
    recognizer.save("TrainingImageLabel/Trainner.yml")
    res = "Profile Saved Successfully"
    message1.configure(text=res)
    message.configure(text=f'Total Registrations till now  : {str(ID[0])}')


def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    IDs = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        IDs.append(ID)
    return faces, IDs


def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")
    for k in tv.get_children():
        tv.delete(k)
    msg = ""
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    exists3 = os.path.isfile("TrainingImageLabel/Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel/Trainner.yml")
    else:
        mess.showerror(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    exists1 = os.path.isfile("StudentDetails/StudentDetails.csv")
    if exists1:
        df = pd.read_csv("StudentDetails/StudentDetails.csv")
    else:
        mess.showerror(title='Details Missing', message='Students details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
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
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID = str(ID)
                aa = str(aa)
                msg = str(ID + "-" + aa)
                attendance = [str(ID), '', aa, '', str(date), '', str(timeStamp)]
                tv.insert('', 0, text=serial, values=(str(ID), str(aa), str(date), str(timeStamp)))
            else:
                serial = 'Unknown'
                msg = str(serial)
            if conf > 75:
                noOfFile = len(os.listdir("ImagesUnknown")) + 1
                cv2.imwrite(f"ImagesUnknown/Image{noOfFile}.jpg", im[y:y + h, x:x + w])
            cv2.putText(im, str(msg), (x, y + h), font, 1, (255, 255, 255), 2)
        cv2.imshow('Taking Attendance', im)
        if cv2.waitKey(1) == ord('q'):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile(f"Attendance/Attendance_{date}.csv")
    if exists:
        with open(f"Attendance/Attendance_{date}.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            for l in attendance:
                writer.writerow(l)
    else:
        with open(f"Attendance/Attendance_{date}.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            for l in attendance:
                writer.writerow(l)
    cam.release()
    cv2.destroyAllWindows()
    res = tv.get_children()
    for i in res:
        tv.delete(i)
    tv.insert('', 0, text=serial, values=(str(ID), str(aa), str(date), str(timeStamp)))


def quit():
    window.destroy()


######################################## UI Setup ###########################################

window = ctk.CTk()
window.geometry("1280x720")
window.resizable(True, False)
window.title("Face Recognition Attendance System")
window.configure(fg_color="white")

clock = ctk.CTkLabel(window, text="00:00:00", fg_color="white", text_color="black", font=('comic', 25, 'bold'))
clock.place(x=1200, y=10)

head1 = ctk.CTkLabel(window, text="Face Recognition Attendance System", fg_color="white", text_color="black", font=('comic', 25, 'bold'))
head1.place(x=400, y=10)

frame1 = ctk.CTkFrame(window, fg_color="white", width=400, height=500)
frame1.place(x=50, y=100)

frame2 = ctk.CTkFrame(window, fg_color="white", width=600, height=500)
frame2.place(x=500, y=100)

frame3 = ctk.CTkFrame(window, fg_color="white", width=200, height=500)
frame3.place(x=1150, y=100)

head2 = ctk.CTkLabel(frame1, text="New User Registration", fg_color="white", text_color="black", font=('comic', 20, 'bold'))
head2.grid(row=0, column=0, padx=20, pady=20)

lbl = ctk.CTkLabel(frame1, text="Enter ID", fg_color="white", text_color="black", font=('comic', 12, 'bold'))
lbl.grid(row=1, column=0, padx=20, pady=20)

txt = ctk.CTkEntry(frame1, width=180, fg_color="white", text_color="black", font=('comic', 12, 'bold'), border_width=1)
txt.grid(row=1, column=1, padx=20, pady=20)

lbl2 = ctk.CTkLabel(frame1, text="Enter Name", fg_color="white", text_color="black", font=('comic', 12, 'bold'))
lbl2.grid(row=2, column=0, padx=20, pady=20)

txt2 = ctk.CTkEntry(frame1, width=180, fg_color="white", text_color="black", font=('comic', 12, 'bold'), border_width=1)
txt2.grid(row=2, column=1, padx=20, pady=20)

message1 = ctk.Label(frame2, text="1)Take Images  >>>  2)Save Profile" ,bg="#c79cff" ,fg="black"  ,width=39 ,height=1, activebackground = "#3ffc00" ,font=('comic', 15, ' bold '))
message1.place(x=7, y=230)

message = ctk.Label(frame2, text="" ,bg="#c79cff" ,fg="black"  ,width=39,height=1, activebackground = "#3ffc00" ,font=('comic', 16, ' bold '))
message.place(x=7, y=450)

clearButton = ctk.CTkButton(frame1, text="Clear", command=clear, fg_color="#f00", text_color="black", font=('comic', 10, 'bold'))
clearButton.grid(row=3, column=0, padx=20, pady=20)

takeImg = ctk.CTkButton(frame1, text="Take Images", command=TakeImages, fg_color="#0f0", text_color="black", font=('comic', 10, 'bold'))
takeImg.grid(row=3, column=1, padx=20, pady=20)

trainImg = ctk.CTkButton(frame1, text="Save Profile", command=psw, fg_color="#0f0", text_color="black", font=('comic', 10, 'bold'))
trainImg.grid(row=4, column=1, padx=20, pady=20)

head3 = ctk.CTkLabel(frame2, text="Mark Attendance", fg_color="white", text_color="black", font=('comic', 20, 'bold'))
head3.grid(row=0, column=0, padx=20, pady=20)

trackImg = ctk.CTkButton(frame2, text="Track Images", command=TrackImages, fg_color="#00fcca", text_color="black", font=('comic', 10, 'bold'))
trackImg.grid(row=1, column=0, padx=20, pady=20)

head4 = ctk.CTkLabel(frame3, text="Registered Students", fg_color="white", text_color="black", font=('comic', 20, 'bold'))
head4.grid(row=0, column=0, padx=20, pady=20)

quitWindow = ctk.CTkButton(frame3, text="Quit", command=quit, fg_color="red", text_color="black", font=('comic', 10, 'bold'))
quitWindow.grid(row=1, column=0, padx=20, pady=20)

window.mainloop()
