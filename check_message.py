"""
Stingy OLX ad message forwarder: check for new message(s) and send them to your email
@author yohanes.gultom@gmail.com
"""

from stingy_olx import StingyOLX
import re
import argparse
import smtplib

email_tpl = '''From: {0}\r\nTo: {1}\r\nSubject: {2}\r\nMIME-Version: 1.0\r\nContent-Type: text/html\r\n\r\n
{3}
'''

message_group_tpl = '''
<strong><a href="{}">{}</a></strong>
{}
'''

message_tpl = '''
<div style="padding-bottom:5px">
  <em>{} ({})</em>
 <div>{}</div>
</div>
'''


def send_email(smtp_config, to, body):
    server_ssl = smtplib.SMTP_SSL(smtp_config['server'], smtp_config['port'])
    server_ssl.ehlo()
    server_ssl.login(smtp_config['username'], smtp_config['password'])
    email = email_tpl.format(
        smtp_config['from'],
        to,
        smtp_config['subject'],
        body,
    )
    server_ssl.sendmail(smtp_config['from'], to, email)
    server_ssl.close()
    print('Email sent')


def build_email(ads):
    """
    Build HTML email format based on template and ad messages
    """
    email = []
    for ad in ads:
        html_messages = []
        for msg in ad['messages']:
            html_messages.append(message_tpl.format(msg['sender'], msg['time'], msg['body']))
        email.append(message_group_tpl.format(ad['url'], ad['title'], '\n'.join(html_messages)))
    return '\n'.join(email)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("olx_username", help="OLX username")
    parser.add_argument("olx_password", help="OLX password")
    parser.add_argument("smtp_username", help="SMTP username")
    parser.add_argument("smtp_password", help="SMTP password")
    parser.add_argument("email_to", help="Email recipient")
    parser.add_argument("-s", "--smtp_server", help="SMTP server", default="smtp.gmail.com")
    parser.add_argument("-p", "--smtp_port", help="SMTP port", type=int, default=465)
    args = parser.parse_args()

    smtp_config = {
        'username': args.smtp_username,
        'password': args.smtp_password,
        'server': args.smtp_server,
        'port': args.smtp_port,
        'from': 'Stingy OLX Message Checker',
        'subject': 'New message in Stingy OLX'
    }

    olx = StingyOLX()
    olx.login(args.olx_username, args.olx_password)
    ads = olx.check_unread_message()
    if ads:
        email = build_email(ads)
        send_email(smtp_config, args.email_to, email)
    olx.logout()

if __name__ == '__main__':
    main()
