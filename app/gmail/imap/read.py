import os
import imaplib


IMAP_SERVER = "imap.gmail.com"

USERNAME = os.environ.get("LIS_GMAIL")
PASSWORD = os.environ.get("LIS_APP_PW")

IN_FOLDER = "new-job-alerts"


def get_emails():
    server = imaplib.IMAP4_SSL(IMAP_SERVER)
    server.login(USERNAME, PASSWORD)

    list_server = server.list()
    print("List of mailboxes:\n{}\n".format(list_server))

    status, messages = server.select(IN_FOLDER)
    print("Mailbox selection status:", status)

    if os.environ.get('ENVIRONMENT', None) == "PRODUCTION":
        num_messages = int(messages[0])
    else:
        num_messages = 3 
    print("Number of messages to read:", num_messages)

    mails = []

    for i in range(1, num_messages+1):
        status, msg = server.fetch(str(i), '(RFC822)')
        print("{}: Email retrieval status: {}".format(i, status))

        mails.append(msg)

    return mails


if __name__ == "__main__":
    emails = get_emails()
