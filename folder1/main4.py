import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import os
import cv2
import numpy as np
import pandas as pd
import datetime
import time


import customtkinter as ctk
from tkinter import ttk  # Import ttk for Treeview
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd                       #if you enter wrong input 

import cv2,os                      #opencv library ; process images ; allow to read , write and add filter in images 
import csv 
import numpy as np
from PIL import Image
import pandas as pd
import  datetime
import time 






# Initialize the window using customtkinter
window = ctk.CTk()
window.geometry("1024x768")
window.title("Face Recognition Attendance System")

# Title label
title_label = ctk.CTkLabel(window, text="Face Recognition Attendance System", font=("Arial", 24))
title_label.grid(row=0, column=0, columnspan=4, pady=10, sticky="n")

# ID Entry
id_label = ctk.CTkLabel(window, text="Enter ID", font=("Arial", 18))
id_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
id_entry = ctk.CTkEntry(window, width=300, height=40)
id_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

# Name Entry
name_label = ctk.CTkLabel(window, text="Enter Name", font=("Arial", 18))
name_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
name_entry = ctk.CTkEntry(window, width=300, height=40)
name_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Department Entry
department_label = ctk.CTkLabel(window, text="Enter Department", font=("Arial", 18))
department_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
department_entry = ctk.CTkEntry(window, width=300, height=40)
department_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

# Buttons (organized in a vertical layout)
take_images_button = ctk.CTkButton(window, text="Take Images", width=200, command=lambda: take_images(id_entry.get(), name_entry.get(), department_entry.get()))
take_images_button.grid(row=1, column=2, padx=20, pady=10)

save_profile_button = ctk.CTkButton(window, text="Save Profile", width=200, command=save_profile)
save_profile_button.grid(row=2, column=2, padx=20, pady=10)

take_attendance_button = ctk.CTkButton(window, text="Take Attendance", width=200, command=mark_attendance)
take_attendance_button.grid(row=3, column=2, padx=20, pady=10)

clear_button_1 = ctk.CTkButton(window, text="Clear", width=200, fg_color="red", command=lambda: id_entry.delete(0, tk.END))
clear_button_1.grid(row=1, column=3, padx=20, pady=10)

clear_button_2 = ctk.CTkButton(window, text="Clear", width=200, fg_color="red", command=lambda: name_entry.delete(0, tk.END))
clear_button_2.grid(row=2, column=3, padx=20, pady=10)

quit_button = ctk.CTkButton(window, text="Quit", width=200, fg_color="red", command=window.quit)
quit_button.grid(row=4, column=2, padx=20, pady=10)

# Table
table_frame = ctk.CTkFrame(window)
table_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="w")
table = ctk.CTkLabel(table_frame, text="Table goes here", width=600, height=200)
table.pack()

# Image and Attendance Logic
def take_images(id, name, department):
    if id == "" or name == "" or department == "":
        messagebox.showerror("Error", "All fields are required!")
        return
    # Your logic for capturing images
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def face_extractor(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        if faces is ():
            return None
        for (x, y, w, h) in faces:
            cropped_face = img[y:y + h, x:x + w]
        return cropped_face

    cap = cv2.VideoCapture(0)
    img_id = 0
    while True:
        ret, frame = cap.read()
        if face_extractor(frame) is not None:
            img_id += 1
            face = cv2.resize(face_extractor(frame), (200, 200))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            file_name_path = "dataset/user." + str(id) + "." + str(img_id) + ".jpg"
            cv2.imwrite(file_name_path, face)
            cv2.putText(frame, str(img_id), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Face Cropper", frame)
        else:
            messagebox.showwarning("No Face Found", "Face not found! Please try again.")
            pass
        if cv2.waitKey(1) == 13 or int(img_id) == 100:  # 100 images for each person
            break
    cap.release()
    cv2.destroyAllWindows()
    messagebox.showinfo("Result", "Images collected successfully!")

def save_profile():
    id = id_entry.get()
    name = name_entry.get()
    department = department_entry.get()
    if id == "" or name == "" or department == "":
        messagebox.showerror("Error", "All fields are required!")
    else:
        with open("student_profiles.csv", "a") as f:
            f.write(f"{id},{name},{department}\n")
        messagebox.showinfo("Result", "Profile saved successfully!")

def mark_attendance():
    def detect_face_and_recognize():
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('trainer.yml')  # Pre-trained model file
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Reading profiles from the CSV file
        student_data = pd.read_csv("student_profiles.csv")
        names = {}
        for _, row in student_data.iterrows():
            names[int(row['ID'])] = row['Name']

        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100))

            for (x, y, w, h) in faces:
                id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

                if confidence < 50:  # Confidence level; lower is better (below 50 indicates a match)
                    name = names.get(id, "Unknown")
                    mark_attendance_in_file(id, name)
                    cv2.putText(frame, f"{name} ({round(100 - confidence)}%)", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    cv2.putText(frame, "Unknown", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

            cv2.imshow("Face Recognition", frame)
            if cv2.waitKey(1) == 13:  # Press 'Enter' to exit
                break

        cap.release()
        cv2.destroyAllWindows()

    def mark_attendance_in_file(id, name):
        with open("attendance.csv", "r+") as file:
            attendance_list = file.readlines()
            attended_ids = [line.split(",")[0] for line in attendance_list]

            if str(id) not in attended_ids:
                now = datetime.datetime.now()
                timestamp = now.strftime("%H:%M:%S")
                date = now.strftime("%Y-%m-%d")
                file.write(f"{id},{name},{date},{timestamp}\n")
                messagebox.showinfo("Attendance", f"Attendance marked for {name}.")

    detect_face_and_recognize()


window.mainloop()
