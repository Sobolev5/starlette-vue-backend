import os
import sys

path = os.path.dirname(os.path.abspath(__file__))
path = path.replace("/apps/mailer", "")
sys.path.insert(0, path)

# help with template rendering
import jinja2
from mailjet_rest import Client

# import of my secret keys for mailjet
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from settings import MAILJET_API_KEY
from settings import MAILJET_API_SECRET


class Mailer:

    """
    Class sends letters to users.
    Use send_email() method as entry point.

    sender - From whom the letter was sent.
    recipient_list - To whom the letter was sent.
    subject - Title of the letter.
    letter_body - Your letter (can use html<> tags)
    mail_service - Optional attribute.
    Use a letter sending service ({'mail_service':'mailjet'}' or add your service. 
        The default mail service is 'mailjet'.
    outcoming_mail - The value of this variable will contain a template
        with the body of the letter and will be sent using mail service.
    """

    def __init__(self, sender: str, recipient_list: list, subject: str = "", letter_body: str = "", mail_service: str = "mailjet", **kwargs):

        self.sender = sender
        self.recipient_list = recipient_list
        self.subject = subject
        self.letter_body = letter_body
        self.mail_service = mail_service
        self.kwargs = kwargs
        self.outcoming_mail: str = ""

    def send_email(self):

        """
        Entry point.

        """

        self._template_render()

        if self.mail_service == "mailjet":
            self._send_mailjet()

    def _template_render(self):

        """
        The method substitutes the necessary data in the HTML template.

        """

        # use jinja2 library and default template (you can change to other html template)
        templateLoader = jinja2.FileSystemLoader(searchpath=f"{path}/templates/mailer")
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "mail_template.html"
        template = templateEnv.get_template(TEMPLATE_FILE)
        self.outcoming_mail = template.render(letter_body=self.letter_body)

    def _send_mailjet(self):

        """
        Sending messages using the Mailjet service.
        """

        api_key = MAILJET_API_KEY
        api_secret = MAILJET_API_SECRET
        mailjet = Client(auth=(api_key, api_secret), version="v3.1")
        data = {
            "Messages": [
                {
                    "From": {
                        "Email": f"{self.sender}",
                        # "Name": ""
                    },
                    "To": [
                        {
                            "Email": f"{self.recipient_list}",
                            # "Name": ""
                        }
                    ],
                    "Subject": f"{self.subject}",
                    # "TextPart": f"{self.message}",
                    "HTMLPart": f"{self.outcoming_mail}",
                    # "CustomID": "AppGettingStartedTest"
                }
            ]
        }
        result = mailjet.send.create(data=data)

        print(result.status_code)
        print(result.json())


# __________________________________________________________________________________________________
# The code below is just for TEST - delete in production

mailer_message_1 = Mailer(sender="evgeniy.markulchak@gmail.com", recipient_list=("drunk_knight@mail.ru"), subject="Welcome to Monitor Project!", letter_body="You are welcome Crazy_Oleg_93! <b>This is bold text for html testing.</b>",)
mailer_message_1.send_email()
