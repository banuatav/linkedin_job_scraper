import os
import collections
import uuid

from . import data, imap_actions

# Data Class
EMAIL_FIELDS = ["id", "subject", "sender", "date", "body", "body_alert", "body_jobs"]
EmailData = collections.namedtuple("EmailData", EMAIL_FIELDS)

class EmailReader:
    def __init__(self, inbox_name=imap_actions.INBOX_FOLDER, destination_folder=imap_actions.DESTINATION_FOLDER):
        self.inbox_name = inbox_name
        self.destination_folder = destination_folder
        self.server = imap_actions.connect()
        self.mails = []

        imap_actions.create_mailbox(self.server, self.destination_folder)
        self.list_mailboxes(verbose=True)

    def list_mailboxes(self, verbose=False):
        list_server = imap_actions.list_mailboxes(self.server)
        if verbose:
            print("\nList of mailboxes:\n{}\n".format(list_server))
        return list_server

    def process_emails(self):
        print("Selecting emails from mailbox: {}".format(self.inbox_name))
        mails_ids = imap_actions.select_mailbox(self.server, self.inbox_name)
        print("Number of emails available:{}\n".format(len(mails_ids)))
        
        if not os.environ.get('PRODUCTION', None) == 'TRUE' and len(mails_ids) > 3:
            mails_ids = mails_ids[:3]
            print("Environment variable PRODUCTION not set TRUE, truncating number of read messages to {}.\n".format(len(mails_ids)))
            
        for id in mails_ids:
            status, msg = imap_actions.fetch_email(id, self.server)
            imap_actions.move_email(self.server, id, self.destination_folder)

            if status !="OK":
                print("{}: Email retrieval status: {}".format(id, status))
            else:
                extracted_data = data.extract_data(msg)
                self.mails.append(EmailData(id=str(uuid.uuid1()), **extracted_data))
        
        imap_actions.disconnect(self.server)
        return self.mails

