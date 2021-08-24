import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Union, List


class Email:
    _server = None

    def send_email(self, sender: str = "Memento Daily Validator",
                   sender_email: str = "daily@mementoweb.org",
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
            self._server.sendmail(sender_email, receiver, message.as_string())

    def close(self):
        self._server.close()


class UnsecureEmail(Email):

    def __init__(self, host="localhost", port=0):
        super().__init__()
        try:
            self._server = smtplib.SMTP(host, port=port)
        except Exception as e:
            print(e)
            raise EmailServerError()


class SecureEmail(Email):
    _server = None

    def __init__(self, host="localhost", port=0, username="", password=""):
        super().__init__()
        try:
            self._server = smtplib.SMTP_SSL(host, port)
            self._server.login(username, password)
        except Exception as e:
            print(e)
            raise EmailServerError()


class EmailServerError(Exception):
    pass
