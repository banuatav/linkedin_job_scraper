import os
import imaplib
import re

# Defaults
IMAP_SERVER = "imap.gmail.com"

USERNAME = os.environ.get("LIS_GMAIL")
PASSWORD = os.environ.get("LIS_APP_PW")

INBOX_FOLDER = "new-job-alerts"
PATTERN_UID = re.compile(r'\d+ \(UID (?P<uid>\d+)\)')
DESTINATION_FOLDER = "processed-job-alerts"

# Functions
def connect():
    server = imaplib.IMAP4_SSL(IMAP_SERVER)
    server.login(USERNAME, PASSWORD)
    return server

def disconnect(server):
    server.logout()

def list_mailboxes(server):
    return server.list()

def create_mailbox(server, name_mailbox):

    print("Creating additional mailbox: {}".format(name_mailbox))
    server.create(name_mailbox)

def select_mailbox(server, inbox_name):
    status, _ = server.select(inbox_name)

    if status !="OK":
        raise Exception("Could not select mailbox {}".fromat(inbox_name))
        
    status, items = server.search(None, "ALL")
    if status !="OK":
        raise Exception("Could not find ids of emails in mailbox {}".fromat(inbox_name))

    ids = items[0].decode().split()
    return ids

def fetch_email(id, server):
    return server.fetch(str(id), '(RFC822)')

def parse_uid(data):
    match = PATTERN_UID.match(data)
    return match.group('uid')

def move_email(server, mail_id, destination_folder=DESTINATION_FOLDER):
    mail_id = str(mail_id)
    copy_status, _ = server.copy(mail_id, destination_folder)
    if copy_status != "OK":
        raise Exception("Could not copy processed email.")
    
    delete_status, _ = server.store(mail_id, '+FLAGS', '\\Deleted')
    if copy_status != "OK":
        raise Exception("Could not delete email.")

    server.expunge()

# Example usage steps
if __name__ == "__main__":
    server = connect()
    _ = list_mailboxes(server)
    mails_ids = select_mailbox(server, INBOX_FOLDER)
    

    if not os.environ.get('ENVIRONMENT', None) == "PRODUCTION":
        num_messages = 3

    print("Number of messages to read:", num_messages)
    
    for id in mails_ids:
        status, msg = fetch_email(id, server)
        print("{}: Email retrieval status: {}".format(id, status))

        move_email(server, id, DESTINATION_FOLDER)

    disconnect(server)