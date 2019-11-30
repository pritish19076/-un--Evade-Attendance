import cv2
import time
import sys
import os
#data=10
vidcount=0
#count2=0
#count1=0
#record=False
#imagePath = sys.argv[0]
#cap = cv2.VideoCapture(0)
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('output.avi',fourcc, 20.0, (1280,720))
#count=0
timeout2=time.time()
import urllib.request
url = "http://192.168.43.221"  # ESP's url, ex: https://192.168.102/ (Esp serial prints it when connected to wifi)
#first=True
#image = cv2.imread('C:\\Users\\Tushar\\AppData\\Local\\Programs\\Python\\Python37-32\\2.jpg')
#gray = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
while True:
    print("I am Here Abhi")
    data=10
    count2=0
    count1=0
    record=True
    imagePath = sys.argv[0]
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    
    count=0
    
    def get_data():
        global data

        n = urllib.request.urlopen(url).read() # get the raw html data in bytes (sends request and warn our esp8266)
        n = n.decode("utf-8") # convert raw html bytes format to string :3
        
        data = int(n)
    while True:
        get_data()
        print("Asking for data again")
        
        if(data==69 and time.time()>timeout2):
            timoeut2=time.time() + 60*2
            record=True
            break

    
    #print("sadbase")
    while record==True:
        if vidcount==0:
            out = cv2.VideoWriter('D:\\PIS\\ESP8266 Node Code\\Captures\\output'+str(vidcount)+'.avi',fourcc, 20.0, (640,480))
            vidcount+=1
            
        elif vidcount==1:
            out = cv2.VideoWriter('D:\\PIS\\ESP8266 Node Code\\Captures\\output'+str(vidcount)+'.avi',fourcc, 20.0, (640,480))
            vidcount-=1
            
        timeout = time.time() + 60*0.17
        while(cap.isOpened()):
            ret, frame = cap.read()
            image=frame
            if ret==True:
                #frame = cv2.flip(frame,0)
                #frame = cv2.flip(frame,0)
                # write the flipped frame
                out.write(frame)
                
                cv2.imshow('frame',frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    record=False
                    break
                if time.time() > timeout:
                    record=False
                    cap.release()
                    out.release()
                    cv2.destroyAllWindows()
                    break
            
            if count%7==0:
                faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
                faces = faceCascade.detectMultiScale(
                    image,
                    scaleFactor=1.3,
                    minNeighbors=1,
                    minSize=(30, 30)
                )

                print("[INFO] Found {0} Faces.".format(len(faces)))

                for (x, y, w, h) in faces:
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    roi_color = image[y:y + h, x:x + w]
                    print("[INFO] Object found. Saving locally.")
                    #if w>100 and h>100 and count<20:
                    cv2.imwrite("D:\\PIS\\ESP8266 Node Code\\Captures\\"+str(count) + '_faces.jpg', roi_color)
                    

                #if count2<20:
                status = cv2.imwrite('D:\\PIS\\ESP8266 Node Code\\Captures\\faces_detected.jpg', image)
                count2+=1
        
                print("[INFO] Image faces_detected.jpg written to filesystem: ", status)
            count1+=1
            count+=1
    if vidcount==1:
        os.startfile(r"D:\PIS\ESP8266 Node Code\FaceRecog.lnk")
    elif vidcount==0:
        os.startfile(r"D:\PIS\ESP8266 Node Code\FaceRecog1.lnk")
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

    

    path = 'D:\\PIS\\ESP8266 Node Code\\Captures\\'
    #print(path)
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.jpg' or '.avi' in file:
                files.append(os.path.join(r, file))
    #for f in files:
    #    print(f)
    print("Emailing....")
    toaddrs_list=['pritish.glt@gmail.com','pritishglt@gmail.com']

    send_mail_gmail('bogus993@gmail.com','kartikgaming',toaddrs_list,'Student Pics','bogus993@gmail.com','Student Data who went out',files)

