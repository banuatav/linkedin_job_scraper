from email import policy
from email.parser import BytesParser
import os
import re


def email_data(file_path):
    with open(file_path, 'rb') as fp:
        msg = BytesParser(policy=policy.default).parse(fp)

    date = msg["DATE"]
    subject = msg["SUBJECT"]
    body = msg.get_body(preferencelist=('plain')).get_content()
    return date, subject, body


def body2job_ads(body):
    body = re.sub(r"-{5,}", "<lb-token>", body)
    jobs = body.split("<lb-token>")

    # Clean none job-ad related data
    jobs = [x for x in jobs if "view job:" in x.lower()]
    return jobs


def details(text, split_link="https://www.linkedin.com"):
    splitted = text.strip().split(split_link)
    text_info = splitted[0].split("\n")
    title, company, location = text_info[:3]
    link = split_link+splitted[1]

    job_details = {"title": title, "company": company,
                   "location": location, "link": link}
    return job_details


def extract(data_folder="data"):
    list_files = os.listdir(data_folder)
    job_ads_detailed = []
    for file in list_files:
        file_path = "data/"+file
        date, subject, body = email_data(file_path)
        unstructured_job_ads = body2job_ads(body)
        for text in unstructured_job_ads:
            structured_data = details(text)
            structured_data["email_date"] = date
            structured_data["email_subject"] = subject
            job_ads_detailed.append(structured_data)
    return job_ads_detailed
