import os
from datetime import datetime
import smtplib
from smtplib import SMTP
from smtplib import SMTPException
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Time Stamps
pic_time = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
fName = pic_time + ".jpg"
command = "raspistill -w 640 -h 640 -vf -hf -o " + fName
os.system(command)

# Email info
usr = 'grandclassifiedteam@gmail.com'
pwd = 'Grand123$'

# Destination email information
toAddr = 'grandclassifiedteam@gmail.com'
fromAddr = usr
sub = 'Image Recorded at ' + pic_time
msg = MIMEMultipart()
msg['Subject'] = sub
msg['From'] = fromAddr
msg['to'] = toAddr
msg.preamble = 'Image Recorded at ' + pic_time

# Email text
body = MIMEText('Image Recorded at ' + pic_time)
msg.attach(body)

# Attach Image
fp = open(fName, 'rb')
img = MIMEImage(fp.read())
fp.close()
msg.attach(img)

# Send Email
s = smtplib.SMTP('smtp.gmail.com', 587)

s.ehlo()
s.starttls()
s.ehlo()

s.login(usr, pwd)
s.sendmail(fromAddr, toAddr, msg.as_string())
s.quit()

print('Email delivered!')
