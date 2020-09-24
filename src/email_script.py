import smtplib
import os
import csv
import sys
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email.mime.multipart import MIMEMultipart
from email import encoders
import pandas as pd
import ssl

#global configuration variables

gmail_name = os.environ.get('PY_GMAIL_ADDR')
gmail_pw = os.environ.get('PY_GMAIL_PW')
resume_filename = "Resume.pdf"

def initialize_email_server():
    conn = smtplib.SMTP('smtp.gmail.com', 587)
    conn.starttls()
    conn.login(gmail_name, gmail_pw)
    return conn


def read_data_clean_it(filepath):
    df = pd.read_csv(filepath)
    df = df.drop_duplicates(subset = ["Contact Email"])
    df = df[['Company', 'Contact Name', 'Contact Email']]
    return df

def loop_df():
    df = read_data_clean_it('data/test_devin.csv')
    print(df.head())
    for row in df.iterrows():
        row = row[1]
        company = row['Company']
        name = row['Contact Name']
        contact_email = row['Contact Email']
        
        message = f"""Hello {name},\nMy name is Devin Link and I am interested in pursuing a career with {company} as a Data Scientist. I am a U.S. citizen and have been working the past year as an Electrical Engineering intern at a small aerial imaging company. I have experience programming complex systems and I deal with hardware and circuit schematics on a daily basis. I have attached my resume, please contact me if you have any questions or opportunities. \nThank you for your time, \nDevin Link"""
        mime_message = MIMEMultipart(From=gmail_name,To=contact_email,Date=formatdate(localtime=True))
        mime_message['Subject'] = f'Looking for career opportunities at {company}' 
        mime_message.attach(MIMEText(message))
        attach_file=MIMEApplication(open(resume_filename, "rb").read())
        encoders.encode_base64(attach_file)
        attach_file.add_header('Content-Disposition','attachment', filename=resume_filename)
        mime_message.attach(attach_file)
        text = mime_message.as_bytes()
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(gmail_name, gmail_pw)
            server.sendmail(gmail_name, contact_email, text)




if __name__ == "__main__":
    # email_password = os.environ.get('PY_GMAIL_PW')
    # email_address = os.environ.get('PY_GMAIL_ADDR')
    # conn = initialize_email_server()
    # # conn.sendmail(email_address,email_address,'Subject: Python TEST\n\nDear Devin,\this is workingi\n dont you think')
    loop_df()
    
    
    