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

    num_messages = int(messages[0])
    print("Number of messages to read:", num_messages)

    status, data = server.fetch('1:{}'.format(num_messages), '(RFC822)')
    print("Email retrieval status:", status)

    return data


if __name__ == "__main__":
    emails = get_emails()
