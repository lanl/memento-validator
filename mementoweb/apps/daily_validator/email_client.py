#
#  Copyright (c) 2021. Los Alamos National Laboratory (LANL).
#  Written by: Bhanuka Mahanama (bhanuka@lanl.gov)
#                     Research and Prototyping Team, SRO-RL,
#                     Los Alamos National Laboratory
#
#  Correspondence: Lyudmila Balakireva, PhD (ludab@lanl.gov)
#                     Research and Prototyping Team, SRO-RL,
#                     Los Alamos National Laboratory
#
#  See LICENSE in the project root for license information.
#

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Union, List


class Email:
    """

        Provides abstract functions of sending an email using an existing email server connection.

    """
    _server = None

    def send_email(self, sender: str = "Memento Daily Validator",
                   sender_email: str = "daily@mementoweb.org",
                   subject: str = "Daily Validator Report",
                   receiver: Union[str, List[str]] = "",
                   html_message: str = ""):
        """

        Sends an email given as a string to recipients.

        :param sender: Name of the sender (Name to appear at the recipient). Defaults to "Memento Daily Validator".
        :param sender_email:
        :param subject: Subject of the email. Defaults to "Daily Validator Report".
        :param receiver: List containing recipient email addresses.
        :param html_message: Message needs to be sent as an HTML text.
        :return: None
        """

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
    """

        Provides interface for establishing unsecure email server connections, or local instances.
        Uses SMTP.

    """

    def __init__(self, host="localhost", port=0):
        super().__init__()
        try:
            self._server = smtplib.SMTP(host, port=port)
        except Exception as e:
            print(e)
            raise EmailServerError()


class SecureEmail(Email):
    """

        Provides interface for establishing secure email server connections using username and password.
        Uses SMTP_SSL.

    """
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
