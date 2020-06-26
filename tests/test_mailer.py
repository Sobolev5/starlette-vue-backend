import os
import sys

path = os.path.dirname(os.path.abspath(__file__))
path = path.replace("/tests", "")
sys.path.insert(0, path + "/apps/mailer")
from mailer import Mailer


def test_mailer():
    mailer_message_1 = Mailer(sender="evgeniy.markulchak@gmail.com", recipient_list=("drunk_knight@mail.ru"), subject="Starlette-Vue mailer test", letter_body="<b>Hello world</b>",)
    sending_result = mailer_message_1.send_email()
    assert True
