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
import string

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
    df['PI Email'] = df['PI Email'].apply(lambda x: x.lower())
    df['PI Email'] = df['PI Email'].apply(lambda x: x.strip())
    df = df.drop_duplicates(subset = ["PI Email"])
    df = df[['Company', 'PI Name', 'PI Email']]
    df['PI Name'] = df['PI Name'].apply(lambda x:string.capwords(x))
    df['Company'] = df['Company'].apply(lambda x: x.lower())
    df['Company'] = df['Company'].apply(lambda x: string.capwords(x))
    df['PI Name'] = df['PI Name'].apply(lambda x: x.split(' '))
    
    return df.iloc[81:]

def loop_df(filepath):
    df = read_data_clean_it(filepath)
    print(df.head())
    for row in df.iterrows():
        row = row[1]
        company = row['Company']
        name = row['PI Name'][0]
        contact_email = row['PI Email']
        message = f"""Hello {name},\nMy name is Devin Link and I am interested in pursuing a career with {company} as a Data Scientist or Software Engineer. I am a U.S. citizen and have been working for the past three years as an engineer in the Oil and Gas industry where I worked on complex control systems. I have recently completed a course in Data Science at Galvanize, and I have a B.S. in Mechanical Engineering from Colorado State University. I have attached my resume, please contact me if you have any questions or opportunities. \nThank you for your time, \nDevin Link"""
        mime_message = MIMEMultipart()
        mime_message['To'] = contact_email
        mime_message['From'] = gmail_name
        mime_message['Subject'] = f'Looking for career opportunities at {company}' 
        mime_message.attach(MIMEText(message))
        attach_file=MIMEApplication(open(resume_filename, "rb").read())
        encoders.encode_base64(attach_file)
        attach_file.add_header('Content-Disposition','attachment', filename=resume_filename)
        mime_message.attach(attach_file)
        print(mime_message['To'])
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
    loop_df('data/Colorado.csv')
    # loop_df('data/test_devin.csv')
    # df = read_data_clean_it('data/first_1000_Sea.csv')
    # print(df.loc[3:3,"PI Email"])
    # print(df.loc[4:4,"PI Email"])
    # print(df.loc[3,"PI Email"]== df.loc[4,"PI Email"])
    
    