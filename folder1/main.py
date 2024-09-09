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


############################################## Functions ###############################

#####

def on_enter(event):
    message1.configure(bg_color="#3ffc00")  # Change to hover color

def on_leave(event):
    message1.configure(bg_color="#c79cff")  # Revert to original color


#####

def assure_path_exists(path):
    dir = os,path.dirname(path)                       #check if it exists
    if not os.path.exists(dir):
        os.makedir(dir)                               #create directory
        
        
def tick():
    time_string = time.strftime('%H:%M:%S')            #convert time 
    clock.config(text=time_string)                     #data in gui format
    clock.after(200,tick)                              #update data after every 200 miliseconds
    
    
def contact():
    mess._show(title='Contact us', message="Please contact us on: 'reekparnasen@gmail.com'")    
    
    
def check_haarcascadefile():                                           #checks if file exists or not
    exists = os.path.isfile("/haarcascade_frontalface_default.xml")    #detect to face of person - it took from github - opencv/data/harcascade 
    if exists:
        pass
    else:
        mess._show(title='Some file missing', message="Please contact us for help.")
        window.destroy()
    
    
def save_pass():                                        # its protected with passwords and checks the password
    assure_path_exists("/TrainingImageLabel/")
    exists1 = os.path.isfile("/TrainingImageLabel/password.txt")
    if exists1:
        tf = open("/TrainingImageLabel/password.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show="*")
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set !! Please try again')
        
        else:
            tf = open("/TrainingImageLabel/password.txt","w")
            tf.write(new_pas)
            mess._show(title='Password registered', message='New Password was registered successfully !!')
            return
        
        
    op = (old.get())                                   # to change the password
    newp = (new.get())
    nnewp = (nnew.get())
    if (op == key):                                    # comparing the key 
        if(newp == nnewp):
            txf = open("/TrainingImageLabel/password.txt","w")
            txf.write(newp)
        else:
            mess._show(title='Error', message="Confirm new password again !!")
            return
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')
        return
    mess._show(title='Password changed', message='Password changed successfully !!')
    master.destroy()
    
    

def change_pass():
    global master
    master = ctk.CTk()                           # gui window for change password
    master.geometry("400x160")
    master.resizable(False, False)
    master.title("Change Password")
    master.configure(fg_color="white")
    
    lbl4 = ctk.CTkLabel(master, text='    Enter Old Password', fg_color='white', text_color='black', font=('comic', 12, 'bold'))
    lbl4.place(x=10, y=10)
    
    global old
    old = ctk.CTkEntry(master, width=180, fg_color="white", text_color="black", font=('comic', 12, 'bold'), show='*', border_width=1)
    old.place(x=180, y=10)
    
    lbl5 = ctk.CTkLabel(master, text='   Enter New Password', fg_color='white', text_color='black', font=('comic', 12, 'bold'))
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
    
    
def psw():                                                                   # checks the entered password
    assure_path_exists("/TrainingImageLabel/")                               # checks exists or not
    exists1 = os.path.isfile("/TrainingImageLabel/password.txt")                
    if exists1:
        tf = open("/TrainingImageLabel/password.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found','Please enter a new password below.', show="*")
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("/TrainingImageLabel/password.txt","w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if(password == key):
        TrainImage()
    elif(password == None):
        pass 
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')
        
        

def clear():                                               # clear the input fields and there are the clear buttons
    txt.delete(0,'end')
    res = "1)Take Images  >>>  2)Save Profile"     
    message1.configure(txt=res)

def clear2():
    txt2.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)   
    
    

def TakeImages():                                                          # take new registrations and newusers images
    check_haarcascadefile()
    columns = ['SERIAL NO.','','ID','','NAME']
    assure_path_exists("/StudentDetails/")
    assure_path_exists("/TrainingImages/")
    serial = 0
    exists = os.path.isfile("/StudentDetails/StudentDetails.csv")
    if exists:
        with open("StudentDetails/StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial //2)
        csvFile1.close()
    else:
        with open("StudentDetails/StudentDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    Id = (txt.get())
    name = (txt2.get())
    if ((name.isalpha()) or (' ' in name)):
        cam =cv2.VideoCapture(0)                                                        # open the webcam        # if there are 2 cam , then value can be 0 or 1 
        haarcascadePath = "/haarcascade_frontalface_default.xml"                        # took data from haarcascade file
        detector = cv2.CascadeClassifier(haarcascadePath)                               # and use camera and haarcascade classifier , in order to map harcascade features to detect face , its a person or not 
        sampleNum = 0                                                                   # keep counting the images from 0 
        while (True):                                                                   # camera is open or not 
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                                # convert rgb to gray scale
            faces = detector.detectMultiScale(gray, 1.3, 5)                             # map out the pixels (color, thickness layer, speed rate )
            for (x, y, w, h) in faces:                                                  # x-axis = width, y-axis = height , needs to calculate data in total face structure
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)                  # height and width also 255, 0, 0 is the color (255 = blue) code for rectangular box , 2 is the thickness of rectangular box
                sampleNum = sampleNum + 1                                               # incrementing sampleNum for taking another sample
                cv2.imwrite("/TrainingImages/" + name + "." + str(serial) + "." + str(sampleNum) + ".jpg", gray[y:y +h, x:x +  w])           # store the images here with details
            cv2.imshow('Taking Images', img)                                            # msg 
            if cv2.waitKey(100) & 0xFF == ord('q'):                                     # stop image clicking upto 100 images , q = quit , 0xFF = used for quiting the camera
                break                                                                        
            elif sampleNum > 100:
                break
        cam.release()                                                       # release video capture camera
        cv2.destroyAllWindows()                                             # close all windows
        res = "Images Taken for ID : " + Id                                 # msg
        row = [serial,'',Id,'',name]                                        # keep track of data
        with open('/StudentDetails/StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
            csvFile.close()
        csvFile.close()
        message1.configure(text=res)
    else:
        if (name .isalpha() == False):
            res = "Enter Correct Name"
            message.configure(text=res)
                


def TrainImage():                                                           # training image
    check_haarcascadefile()                                                 # check that haarcascade file exists or not
    assure_path_exists("/TrainingImageLabel/")                              # check that folder exists or not
    recognizer = cv2.face_LBPHFaceRecognizer.create()                       # algorithm to identify each image uniquely, make out pattern , makes difference between 2 persons faces, sub algorithm
    haarcascadePath = "/haarcascade_frontalface_default.xml"                # taking the checkeedfile
    detector = cv2.CascadeClassifier(haarcascadePath)
    faces, ID = getImagesAndLabels("/TrainingImages/")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return
    recognizer.save("/TrainingImageLabel/Trainner.yml")
    res = "Profile Saved Successfully"
    message1.configure(text = res)
    message.configure(text='Total Registrations till now  : ' + str(ID[0]))
    
    
    
def getImagesAndLabels(path):                                                                # taking a paths directory in order to find out folder locations
    imagePaths = [ os.path.join(path, f) for f in os.listdir(path) ]                         # joining the paths with directory 
    faces = []                                                                               # in array format
    Ids = []
    for imagePath in imagePaths:                                                             # keep looping
        pilImage = Image.open(imagePath).convert('L')                                        # convert into gray scale ( L for pillow libraries)
        imageNp = np.array(pilImage, 'uint8')                                                # map using numpy array, mapping each and every images   
        ID = int(os.path.split(imagePath)[-1].split(".")[1])                                 #
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids    
        
        
        
def TrackImages():
    check_haarcascadefile()
    assure_path_exists("/Attendance/")
    assure_path_exists("/StudentDetails/")
    for k in tv.get_children():
        tv.delete(k)
    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    exists3 = os.path.isfile("/TrainingImageLabel/Trainner.yml")         #what to do 
    if exists3:
        recognizer.read("/TrainingImageLabel/Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    haarcascadePath = "/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(haarcascadePath)
    
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    exists1 = os.path.isfile("/StudentDetails/StudentDetails.csv")
    if exists1:
        df = pd.read_csv("/StudentDetails/StudentDetails.csv")
    else:
        mess._show(title='Details Missing', message='Students details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for(x, y, w, h) in faces:
            cv2.rectangle(im, (x,y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if(conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H-%M-%S")
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values()
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values()
                ID = str(ID)
                bb = str(aa)
                bb = bb[2:-2]
                attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp)]
            else:
                Id = 'Unknown'
                bb = str(Id)
            cv2.putText(im, str(bb), (x,y + h), font, 1, (255, 255, 255), 2)                   # take the attandance 
        cv2.imshow("Taking Attandance",im)
        if (cv2.waitKey(1) == ord('q')):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
    exists = os.path.exists(r"\Attendance\Attendance_" + date + ".csv")
    if exists:
        with open(r"\Attendance\Attendance_" + date + ".csv", "a+") as csvFile1:          # printing with current date 
            writer = csv.writer(csvFile1)
            writer.writerow(attendance)                                                 # maps every data in row format
        csvFile1.close()
    else:
        with open(r"\Attendance\Attendance_" + date + ".csv", "a+") as csvFile1:                 
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            writer.writerow(attendance)
        csvFile1.close()
    with open(r"\Attendance\Attendance_" + date + ".csv", "r") as csvFile1:              # other registered person is taking the attandance
        reader1 = csv.reader(csvFile1)
        for lines in reader1:                   # looping based on current index in csv file for mapping
            i = i + 1
            if (i >  1):
                if (i % 2 != 0):
                    iidd = str(lines[0]) + '  ' 
                    tv.insert('', 0, text=iidd, values = (str(lines[2]), str(lines[40]), str(lines[6])))
    csvFile1.close()
    cam.release()
    cv2.destroyAllWindows()
    
    
################################  Used Stuffs ##################################################

global key                                                       # for password
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day, month, year = date.split('-')                              # split the date

mont = {'01':'January',
         '02':'February',
         '03':'March',
         '04':'April',
         '05':'May',
         '06':'June',
         '07':'July',
         '08':'August',
         '09':'September',
         '10':'October',
         '11':'November',
         '12':'December'
}                  
            
######################################## GUI ############################################        
        
window = ctk.CTk()
window.geometry("1280x720")                                          # screen size / screen resolution
window.resizable(True, False)                                        # resize / maximize window / minimize window
window.title("Attendance System")
window.configure(background = '#2d420a')                             # mapping the gui color 

frame1 = ctk.CTkFrame(window, bg_color='#c79cff')                     # conponents
frame1.place(relx=0.11, rely=0.17, relwidth=0.39, relheight=0.80)

frame2 = ctk.CTkFrame(window, bg_color='#c79cff')
frame2.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.80)      

message3 = ctk.CTkLabel(window, text="Face Recognition Based Attendance System", width=55, height=1, font=('comic', 29, 'bold'))
message3.place(x=10, y=10)
        
frame3 = ctk.CTkFrame(window, bg_color='#c4c6ce')
frame3.place(relx=0.52, rely=0.09, relwidth=0.09, relheight=0.07) 

frame4 = ctk.CTkFrame(window, bg_color='#c4c6ce')
frame4.place(relx=0.36, rely=0.09, relwidth=0.16, relheight=0.07)   

datef = ctk.CTkLabel(frame4, text = day + "-" + mont[month] + "-" + year + " | ", fg_color='#ff61e5', bg_color = '#2d420a', width=55, height=1, font=('comic', 27, 'bold')) 
datef.pack(fill='both', expand=1)

clock = ctk.CTkLabel(frame3, fg_color='#ff61e5', bg_color='#2d420a', width=55, height=1, font=('comic', 29, 'bold'))
clock.pack(fill="both", expand=1)

head2 = ctk.CTkLabel(frame2, text="                       For New Registrations                       ", fg_color="black",bg_color="#00fcca" ,font=('comic', 17, 'bold'))
head2.grid(row=0,column=0)

head1 = ctk.CTkLabel(frame1, text="                       For Already Registered                       ", fg_color="black",bg_color="#00fcca" ,font=('comic', 17, 'bold'))
head1.place(x=0,y=0)

lbl = ctk.CTkLabel(frame2, text="Enter ID",width=20  ,height=1  ,fg_color="black"  ,bg_color="#c79cff" ,font=('comic', 17, 'bold'))
lbl.place(x=80, y=55)

txt = ctk.CTkEntry(frame2,width=32 ,fg_color="black",font=('comic', 15, 'bold'))
txt.place(x=30, y=88)

lbl2 = ctk.CTkLabel(frame2, text="Enter Name",width=20  ,fg_color="black"  ,bg_color="#c79cff" ,font=('comic', 17, 'bold'))
lbl2.place(x=80, y=140)

txt2 = ctk.CTkEntry(frame2,width=32 ,fg_color="black",font=('comic', 15, 'bold')  )
txt2.place(x=30, y=173)

message1 = ctk.CTkLabel(frame2, text="1)Take Images  >>>  2)Save Profile" ,bg_color="#c79cff" ,fg_color="black"  ,width=39 ,height=1, font=('comic', 15, 'bold'))
message1.place(x=7, y=230)

# Bind mouse enter and leave events
message1.bind("<Enter>", on_enter)
message1.bind("<Leave>", on_leave)

message = ctk.CTkLabel(frame2, text="" ,bg_color="#c79cff" ,fg_color="black"  ,width=39,height=1, font=('comic', 16, 'bold'))
message.place(x=7, y=450)

# Bind mouse enter and leave events
message.bind("<Enter>", on_enter)
message.bind("<Leave>", on_leave)

lbl3 = ctk.CTkLabel(frame1, text="Attendance",width=20  ,fg_color="black"  ,bg_color="#c79cff"  ,height=1 ,font=('comic', 17, 'bold'))
lbl3.place(x=100, y=115)
   
        
res = 0                                                     # calculate attendance 
exists = os.path.exists("/StudentDetails/StudentDetails.csv")
if exists:
    with open("/StudentDetails/StudentDetails.csv", 'r') as  csvFile1:              #reading
        reader1 = csv.reader(csvFile1)
        for l in reader1:                      # reads data
            res = res + 1
        res = (res // 2) - 1
        csvFile1.close()
else:
    res = 0            
message.configure(text = "Total Registrations till now : " + str(res))              #print total attendance   


################################## Menu Bar for Tkinter #################################

 

# menubar = ctk.Menu(window,relief='ridge')
# filemenu = ctk.Menu(menubar,tearoff=0)
# filemenu.add_command(label='Change Password', command = change_pass)
# filemenu.add_command(label='Contact Us', command = contact)
# filemenu.add_command(label='Exit',command = window.destroy)
# menubar.add_cascade(label='Help',font=('comic', 29, 'bold'),menu=filemenu)


                ##############   Menu Bar for Customtkinter    #####################
                          
def on_option_select(value):
    if value == "Change Password":
        change_pass()
    elif value == "Contact Us":
        contact()
    elif value == "Exit":
        window.destroy()       
        
# Create a frame for the option menu
menu_frame = ctk.CTkFrame(window, height=40)
menu_frame.pack(fill="x", side="top")

# Create an option menu with the choices
options = ["Change Password", "Contact Us", "Exit"]
option_menu = ctk.CTkOptionMenu(menu_frame, values=options, command=on_option_select)
option_menu.pack(padx=10, pady=10)

# Create a frame for the main content
main_frame = ctk.CTkFrame(window)
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

# Add other customtkinter widgets to the main frame
label = ctk.CTkLabel(main_frame, text="Help", font=('comic', 15, 'bold'))
label.pack()                  



################## TREEVIEW ATTENDANCE TABLE ####################

tv = ttk.Treeview(frame1, height=13, columns=('name', 'date', 'time'))
tv.column('#0',width=82)
tv.column('name',width=130)
tv.column('date',width=133)
tv.column('time',width=133)
tv.grid(row=2,column=0,padx=(0,0),pady=(150,0),columnspan=4)
tv.heading('#0',text ='ID')
tv.heading('name',text ='NAME')
tv.heading('date',text ='DATE')
tv.heading('time',text ='TIME')

###################### SCROLLBAR ################################

scroll=ctk.CTkScrollbar(frame1,orient='vertical',command=tv.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(150,0),sticky='ns')
tv.configure(yscrollcommand=scroll.set)

###################### BUTTONS ##################################

clearButton = ctk.Button(frame2, text="Clear", command=clear  ,fg_color="black"  ,bg_color="#ff7221"  ,width=11 ,activebackground = "white" ,font=('comic', 11, 'bold'))
clearButton.place(x=335, y=86)
clearButton2 = ctk.Button(frame2, text="Clear", command=clear2  ,fg_color="black"  ,bg_color="#ff7221"  ,width=11 , activebackground = "white" ,font=('comic', 11, 'bold'))
clearButton2.place(x=335, y=172)    
takeImg = ctk.Button(frame2, text="Take Images", command=TakeImages  ,fg_color="white"  ,bg_color="#6d00fc"  ,width=34  ,height=1, activebackground = "white" ,font=('comic', 15, 'bold'))
takeImg.place(x=30, y=300)
trainImg = ctk.Button(frame2, text="Save Profile", command=psw ,fg_color="white"  ,bg_color="#6d00fc"  ,width=34  ,height=1, activebackground = "white" ,font=('comic', 15, 'bold'))
trainImg.place(x=30, y=380)
trackImg = ctk.Button(frame1, text="Take Attendance", command=TrackImages  ,fg_color="black"  ,bg_color="#3ffc00"  ,width=35  ,height=1, activebackground = "white" ,font=('comic', 15, 'bold'))
trackImg.place(x=30,y=50)
quitWindow = ctk.Button(frame1, text="Quit", command=window.destroy  ,fg_color="black"  ,bg_color = "#eb4600"  ,width=35 ,height=1, activebackground = "white" ,font=('comic', 15, 'bold'))
quitWindow.place(x=30, y=450)

##################### END ######################################

# window.configure(menu=menubar)
window.mainloop()

####################################################################################################

        
