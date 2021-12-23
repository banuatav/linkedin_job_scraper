import os
import collections
import uuid

from . import data, imap_actions

# Data Class
EMAIL_FIELDS = ["id", "subject", "sender", "date", "body", "body_alert", "body_jobs"]
EmailData = collections.namedtuple("EmailData", EMAIL_FIELDS)

class EmailReader:
    def __init__(self, inbox_name=imap_actions.INBOX_FOLDER, destination_folder=imap_actions.DESTINATION_FOLDER, max_nr_mails=100):
        self.inbox_name = inbox_name
        self.destination_folder = destination_folder
        self.server = imap_actions.connect()
        self.mails = []

        imap_actions.create_mailbox(self.server, self.destination_folder)
        self.list_mailboxes(verbose=True)

        print("Selecting emails from mailbox: {}".format(self.inbox_name))
        self.mail_ids = imap_actions.select_mailbox(self.server, self.inbox_name)
        
        print("Number of emails available:{}\n".format(len(self.mail_ids)))
        
        if not os.environ.get('ENVIRONMENT', None) == 'PRODUCTION' and len(self.mail_ids) > max_nr_mails:
            self.mail_ids = self.mail_ids[:max_nr_mails]
            print("ENVIRONMENT not set to PRODUCTION, truncating number of read messages to {}.\n".format(len(self.mail_ids)))

    def list_mailboxes(self, verbose=False):
        list_server = imap_actions.list_mailboxes(self.server)
        if verbose:
            print("\nList of mailboxes:\n{}\n".format(list_server))
        return list_server

    def read_email(self, id):
        status, msg = imap_actions.fetch_email(id, self.server)

        if status !="OK":
            print("{}: Email retrieval status: {}".format(id, status))
            raise Exception("Couldnt retrieve email.")
        else:
            extracted_data = data.extract_data(msg)
        
        return EmailData(id=str(uuid.uuid1()), **extracted_data)
    
    def archive_email(self, id):
        imap_actions.move_email(self.server, id, self.destination_folder)

    def disconnect_server(self):
        imap_actions.disconnect(self.server)
