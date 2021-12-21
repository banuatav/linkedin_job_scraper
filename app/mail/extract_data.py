import email
import re

def unpack_header(parsed_msg):
    sender = parsed_msg["from"]
    subject = parsed_msg["subject"]
    date = parsed_msg["date"]
    return subject, sender, date

def unpack_body(parsed_msg):
    if parsed_msg.is_multipart():
        body = ''
        for part in parsed_msg.get_payload():
            if part.get_content_type() == "text/plain":
                body += part.get_payload()
    else:
        body = parsed_msg.get_payload()
    return body

def extract_links(body):
    splitted_body = re.split("-{4,}", body)
    alert = splitted_body[0]
    raw_jobs = splitted_body[1:-2]

    jobs = []
    for job in raw_jobs:
        name, company, location, link = None, None, None, None
        splitted_job = job.strip().split("\r\n")

        if len(splitted_job)>3:
            name, company, location = splitted_job[0:3]
            
        try:
            raw_link = [x for x in splitted_job[4:] if x.strip().lower().startswith("view job")]
            if raw_link:
                link = raw_link[0].split()[-1].rstrip("?alertAction=3D=")
        except Exception as e:
            print(e)
        
        jobs.append({"name":name, "company":company, "location":location, "link":link})
    return alert, jobs

def extract_data(msg):
    for response_part in msg:
        if isinstance(response_part, tuple):
            parsed_msg = email.message_from_bytes(response_part[1])
            subject, sender, date = unpack_header(parsed_msg)
            body = unpack_body(parsed_msg)
            alert, jobs = extract_links(body)
            return {"subject":subject, "sender":sender, "date":date, "body":body, "body_alert":alert, "body_jobs":jobs}