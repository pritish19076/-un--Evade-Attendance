import face_recognition
import cv2
faces=[]
# This is a demo of running face recognition on a video file and saving the results to a new video file.
#
# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Open the input movie file
input_movie = cv2.VideoCapture("Captures\\output1.avi")
length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

# Create an output movie file (make sure resolution/frame rate matches input video!)

# Load some sample pictures and learn how to recognize them.
lmm_image = face_recognition.load_image_file("data\\ayu.jpg")
lmm_face_encoding = face_recognition.face_encodings(lmm_image)[0]

al_image = face_recognition.load_image_file("data\\pri.jpg")
al_face_encoding = face_recognition.face_encodings(al_image)[0]

a2_image = face_recognition.load_image_file("data\\tus.jpg")
a2_face_encoding = face_recognition.face_encodings(a2_image)[0]


known_faces = [
    lmm_face_encoding,
    al_face_encoding,
    a2_face_encoding
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
frame_number = 0

while True:
    # Grab a single frame of video
    ret, frame = input_movie.read()
    frame_number += 1

    # Quit when the input video file ends
    if not ret:
        break

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.50)

        # If you had more than 2 faces, you could make this logic a lot prettier
        # but I kept it simple for the demo
        name = None
        if match[0]:
            name = "Ayush Misra"
        elif match[1]:
            name = "Pritish Gulati"
        elif match[2]:
            name="Tushar Mohan"

        face_names.append(name)
        

    # Label the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        if not name:
            continue

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
        #print("Wrote")
        if name not in faces:
            print("Wrote")
            cv2.imwrite(str(name)+'.jpg', frame)
        if name not in faces:
            faces.append(name)
    # Write the resulting image to the output video file
    print("Loading frame {} / {}".format(frame_number, length))
    

# All done!
print(faces)
input_movie.release()
cv2.destroyAllWindows()

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_mail_gmail(username,password,toaddrs_list,msg_text,fromaddr=None,subject="Test mail",attachment_path_list=None):

	s = smtplib.SMTP('smtp.gmail.com:587')
	s.starttls()
	s.login(username, password)
	#s.set_debuglevel(1)
	msg = MIMEMultipart()
	sender = fromaddr
	recipients = toaddrs_list
	msg['Subject'] = subject
	if fromaddr is not None:
		msg['From'] = sender
	msg['To'] = ", ".join(recipients)
	if attachment_path_list is not None:
		for each_file_path in attachment_path_list:
			try:
				file_name=each_file_path.split("\\")[-1]
				part = MIMEBase('application', "octet-stream")
				part.set_payload(open(each_file_path, "rb").read())

				encoders.encode_base64(part)
				part.add_header('Content-Disposition', 'attachment' ,filename=file_name)
				msg.attach(part)
			except Exception as e:
				print (e)
	msg.attach(MIMEText(msg_text,'html'))
	s.sendmail(sender, recipients, msg.as_string())

import os
path = 'D:\\PIS\\ESP8266 Node Code\\'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
	for file in f:
		if '.jpg' in file and 'Captures' not in r and 'data' not in r:
			files.append(os.path.join(r, file))


    

toaddrs_list=['pritish.glt@gmail.com','pritishglt@gmail.com']
if not (faces==[] or faces==["Unknown"]):
    print("Emailing....")
    send_mail_gmail('bogus993@gmail.com','kartikgaming',toaddrs_list,str(faces),'bogus993@gmail.com','Student Data Who went out Final',files)
