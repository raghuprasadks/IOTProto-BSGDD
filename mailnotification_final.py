import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

def sendMail(msubject,mbody,filename,lang,lat):
    try:
        fromaddr = "bsgddcce3@gmail.com" # created for our project
        toaddr = "prasadraghuks@gmail.com"  # recipient mail id
           
        # instance of MIMEMultipart 
        msg = MIMEMultipart() 
          
        # storing the senders email address   
        msg['From'] = fromaddr 
          
        # storing the receivers email address  
        msg['To'] = toaddr 
          
        # storing the subject  
        msg['Subject'] = msubject +str(lang) + " " +str(lat)
          
        # string to store the body of the mail 
        body = mbody
          
        # attach the body with the msg instance 
        msg.attach(MIMEText(body, 'plain')) 
          
        # open the file to be sent  
        #filename = "20190422164209-loc1.jpg"   # name of the file to be dynamicaly passed( any filetype)
        attachment = open(filename, "rb") # path of the image
          
        # instance of MIMEBase and named as p 
        p = MIMEBase('application', 'octet-stream') 
          
        # To change the payload into encoded form 
        p.set_payload((attachment).read()) 
          
        # encode into base64 
        encoders.encode_base64(p) 
           
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
          
        # attach the instance 'p' to instance 'msg' 
        msg.attach(p) 
          
        # creates SMTP session 
        s = smtplib.SMTP('smtp.gmail.com', 587) 
          
        # start TLS for security 
        s.starttls() 
          
        # Authentication 
        s.login(fromaddr, "bsgdd123") # password
          
        # Converts the Multipart msg into a string 
        text = msg.as_string() 
          
        # sending the mail 
        s.sendmail(fromaddr, toaddr, text) 
        print('mail sent')
          
        # terminating the session 
        s.quit() 
        # -*- coding: utf-8 -*-
    except:
        print('exception occured in mail')

'''
filename = "20190422164209-loc1.jpg"
lang =13.0731511
lat = 77.616761
sendMail("Garbage dump detected @","Garbage dump detected. Please find the attached image for your kind reference",filename,lang,lat)
'''