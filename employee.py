import face_recognition
import cv2
import os
import os.path
from face_recognition.face_recognition_cli import image_files_in_folder
from flask import Flask , request, jsonify, render_template , send_file
import mysql.connector
import datetime
import json
from pandas import DataFrame , ExcelWriter
from collections import OrderedDict
import numpy as np
app=Flask(__name__)






@app.route("/dashboard")
def dashboard():
    return render_template('index.html')


#url for reviewing the attendance data
@app.route('/take_attendance',methods=['GET','POST'])
def fetch_attendance():
    if request.method == "POST":
        date=request.form['date']
       
        list_of_student_id=Face_rec()
        list_of_all_student_id=['161302110','161302007','161302054','161302058','161302068','161302091',]        
        list_of_all_student=["Akshit","Shashank","Piyush","Mridul","Mohit","Saksham"]

  
        b={"status":[]}
        for i in list_of_all_student_id:
            if i in list_of_student_id:
                b["status"].append("present")
            else:
                b["status"].append("absent")
        count_present=0
        count_abs=0
        for i in b["status"]:
            if i =="present":
                count_present+=1
            else:
                count_abs+=1
        
        df=DataFrame(OrderedDict({'student_id':list_of_all_student_id,'student_name':list_of_all_student,'status':b["status"]}))
        df2=DataFrame(OrderedDict({'student_id':[np.nan,np.nan,np.nan],'student_name':[np.nan,np.nan,np.nan],'status':["Total:"+str(len(b["status"])),"Present:"+str(count_present),"Absent:"+str(count_abs)]}))
        df=df.append(df2)
        
        with ExcelWriter('attendance_sheet.xlsx', engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name=date)
        return send_file('/home/akshit/mindmapperz/raspberry_pi/attendance_sheet.xlsx', attachment_filename='attendance_sheet.xlsx')
        
        
           
def Face_rec():
    
    resource= "http://pi:raspberry@192.168.1.15:8160"  
    video_capture = cv2.VideoCapture(resource)

    #To check if the connection is established between channel and opencv
    print('if video_Cap is opened :',str(video_capture.isOpened()))

 
# Create arrays of known face encodings and their names
    if video_capture.isOpened():
        
        known_face_encodings = []
  
        known_face_names = []
    
        SamplePic_dir="employee"    
    # Loop through each person in the training set
        for PersonName in os.listdir(SamplePic_dir):
            if not os.path.isdir(os.path.join(SamplePic_dir, PersonName)):
                continue

    # Loop through each training image for the current person
            for img_path in image_files_in_folder(os.path.join(SamplePic_dir,PersonName)):
                image = face_recognition.load_image_file(img_path)
    
    # Add face encoding for current image to the training set
  
                known_face_encodings.append(face_recognition.face_encodings(image)[0])
                known_face_names.append(PersonName)
        
        print(known_face_names)        

 
# Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        final_names=[]
        process_this_frame = True
        i=0


        while True:
    # Grab a single frame of video
       
            ret, frame = video_capture.read()
        
    # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
            if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
       
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                # original
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding,0.5)
                    name = " "

            # If a match was found in known_face_encodings, just use the first one.
                    if True in matches:
                        first_match_index = matches.index(True)

                        name = known_face_names[first_match_index]
                
                
		          
                    face_names.append(name)

            process_this_frame = not process_this_frame
            print( face_names)
            for x in face_names:
                if x in final_names or x==' ':
                    pass
                else : 
                    final_names.append(x)
            if i>1000:   #This is something i don't want to do it like this 
                break   #but i don't get a threading way to handle this problem of breaking the 
            i+=1        #while loop  if some user want to stop streaming
            

        print(final_names)
        return final_names
    else :
        return "Error : OpenCV connection did not established !"
    
    

if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True,threaded=True)
