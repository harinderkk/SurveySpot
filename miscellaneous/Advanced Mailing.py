import smtplib  # import simple mail transfer protocol library

from email.mime.multipart import MIMEMultipart  # import class for using multipart
from email.mime.text import MIMEText    # import class for attached files

from_address = "Your Mail Address"
to_address = "Sending Address"

msg = MIMEMultipart()   # assign a variable to the multipart class

msg['From'] = 'vshivam532@gmail.com'
msg['To'] = 'vshivam532@gmail.com'
msg['Subject'] = "Multipart"

filename = "test.txt"
with open(filename, 'r') as f:
    message = MIMEText(f.read(), _subtype="txt")
    message.add_header('Content-Disposition', 'Attachment', filename=filename)
    msg.attach(message)

body = "Hi Brother"
msg.attach(MIMEText(body, "plain"))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('vshivam532@gmail.com', '24@shivam@1724&&')
text = msg.as_string()
server.sendmail('vshivam532@gmail.com', 'vshivam532@gmail.com', text)
server.quit()
print("Email Sent Successfully")
