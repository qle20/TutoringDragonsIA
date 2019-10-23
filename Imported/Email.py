
# Standard Library Immports
import os
import sys

# Third party imports
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# Local application imports
sys.path.append("Imported")
from Imported import Connector as cn


def send_email(sender, password, send_to, message):
    '''
    This function only works with the an email address
    that has enable 3rd party connection. To do so...
     '''
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.sendmail(sender, send_to, message)
            server.quit()
    except:
        error = send_to
        return error

def make_single_email(sender, password, send_to, subject, msg):
    '''
    Make message, where the subject, the message  has to be parsed.
    :return: The message as a string.
    '''
    message = f"Subject: {subject}\n\n{msg}"
    error_value = send_email(sender, password, send_to, message)
    if error_value == "NO_LIST":
        return None
    return error_value

def send_attachment(file_location, sender, password, send_to, subject, message):
    '''
    Low Key stole from some guy
    '''
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = send_to
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))
    filename = os.path.basename(file_location)
    attachment = open(file_location, "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # Attach the attachment to the MIMEMultipart object
    msg.attach(part)
    text = msg.as_string()

    error_value = send_email(sender, password, send_to, text)
    if error_value == "NO LIST":
        return None
    return error_value

def send_multiple(sender, password, email_list, subject, message, file_location=None):
    '''

    '''
    error_list = []

    if file_location == None:
        for email in email_list:
            error_value = make_single_email(sender, password, email, subject, message )
            if error_value != "NO LIST":
                error_list.append(error_value)
    else:
        for email in email_list:
            error_value = send_attachment(file_location, sender, password, email, subject, message)
            if error_value != "NO LIST":
                error_list.append(error_value)

    return error_list


if __name__ == "__main__":

    ## initialize
    file_location = '/Users/lequocanh/Documents/GitHub/TutoringDragonsIA/Algorithms/Imported/text.txt'
    user_host = 'localhost'
    user_login = 'root'
    password = 'razzmatazz'
    schema = 'Test_schema'
    subject = "Nani"
    message = '''
     I love CS
     '''

    email_address = os.environ.get("DB_USER")
    email_pass = os.environ.get("DB_PASS")

    ## Accessing database for emails to send to people
    connection, curr = cn.connect(user_host, user_login, password, schema)
    email_list = cn.get_value_list(curr, "Student", 1)
    error = send_multiple(email_address, email_pass, email_list, subject, message)
