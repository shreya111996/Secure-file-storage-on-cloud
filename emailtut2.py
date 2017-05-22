import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

def mail(attachment,image_path,user):
  COMMASPACE = ', '
  fromaddr = "securefileproject@gmail.com"
  #recipients = ['shrreyabisen@gmail.com','radhikalahoti1402@gmail.com','nidhibudhraja554@gmail.com','johnroshni96@gmail.com']
  recipients = [user.email]
  msg = MIMEMultipart()

  msg['From'] = fromaddr
  msg['To'] = COMMASPACE.join(recipients)
  msg['Subject'] = "Image Password"

  body = "Password Image for Decryption"

  msg.attach(MIMEText(body, 'plain'))

  fp = open(image_path, 'rb')
  msg_img = MIMEImage(fp.read())
  fp.close()
  msg_img.add_header('Content-ID', '<{}>'.format('password.jpg'))
  msg.attach(msg_img)

  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  server.login(fromaddr, "decryptsem6")
  text = msg.as_string()
  server.sendmail(fromaddr, recipients, text)
  server.quit()