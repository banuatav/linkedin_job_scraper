from email import policy
from email.parser import BytesParser

def email_data(file_path):
    with open(file_path, 'rb') as fp:
        msg = BytesParser(policy=policy.default).parse(fp)

    date = msg["DATE"]
    subject = msg["SUBJECT"]
    body = msg.get_body(preferencelist=('plain')).get_content()
    return date, subject, body