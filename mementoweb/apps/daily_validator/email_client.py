import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Union, List


class Email:
    _server = None

    def __init__(self, username="", password=""):
        try:
            self._server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            self._server.login(username, password)
        except Exception as e:
            print(e)
            raise EmailServerError()

    def send_email(self, sender: str = "Memento Daily Validator",
                   subject: str = "Daily Validator Report",
                   receiver: Union[str, List[str]] = "",
                   html_message: str = ""):

        if self._server is None:
            raise EmailServerError()
        else:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = sender

            message.attach(MIMEText(html_message, "html"))
            self._server.sendmail(sender, receiver, message.as_string())

    def close(self):
        self._server.close()


class EmailServerError(Exception):
    pass
