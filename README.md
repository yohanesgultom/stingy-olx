## Stingy-OLX

Login to olx.co.id to check for unread messages and forward it to email. All because olx is so stingy.

**Dependency**
* lxml `pip install lxml`
* [Requests](http://docs.python-requests.org) `pip install requests`
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) `pip install bs4`

**Usage**

Command:
```
python check_message.py [-h] [-s SMTP_SERVER] [-p SMTP_PORT] olx_username olx_password smtp_username smtp_password email_to
```

Positional arguments:
```
olx_username          OLX username
olx_password          OLX password
smtp_username         SMTP username
smtp_password         SMTP password
email_to              Email recipient
```

optional arguments:
```
-h, --help: show this help message and exit
-s SMTP_SERVER, --smtp_server: SMTP server
-p SMTP_PORT, --smtp_port: SMTP port
```
