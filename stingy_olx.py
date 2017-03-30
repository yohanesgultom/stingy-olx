"""
Stingy OLX scrapper
@author yohanes.gultom@gmail.com
"""

import bs4
import requests
import re


class StingyOLX:

    def __init__(self):
        self.s = requests.Session()
        self.cookies = {}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
        }
        soup = self.get('http://m.olx.co.id/masuk/')
        login_btn = soup.select('#loginForm input[type=submit]')[0]
        assert login_btn['value'] == 'Masuk'

    def get(self, url):
        r = self.s.get(url, headers=self.headers, cookies=self.cookies, allow_redirects=True)
        self.cookies = r.cookies
        return bs4.BeautifulSoup(r.text, 'lxml')

    def post(self, url, data={}):
        r = self.s.post(url, headers=self.headers, cookies=self.cookies, data=data, allow_redirects=True)
        self.cookies = r.cookies
        return bs4.BeautifulSoup(r.text, 'lxml')

    def login(self, username, password):
        data = {'login[email]': username, 'login[password]': password}
        soup = self.post('http://m.olx.co.id/masuk/', data)
        link = soup.find('a', text=re.compile('^Akun Saya \(\d+\)'))
        assert link.contents[0].startswith('Akun Saya')
        return soup

    def logout(self):
        soup = self.get('http://m.olx.co.id/masuk/logout/')
        link = soup.find('a', text='Akun Saya')
        assert link.contents[0].startswith('Akun Saya')

    def check_unread_message(self):
        soup = self.get('http://m.olx.co.id/iklanku/pesan/?search[unread]=1')
        new_message_links = soup.select('#answersContainer a[href^="http://m.olx.co.id/iklanku/answer"]')
        unread_messages = []
        for new_message_link in new_message_links:
            soup = self.get(new_message_link['href'])
            ad_title = soup.select('strong.medium.color-6')[1].contents[0].strip()
            ad_url = soup.find('a', text=re.compile('^View ad details'))['href']
            conversations = soup.select('ul.conversation li')
            ad_messages = []
            for conversation in conversations:
                sender = conversation.select('h4 span')[0].contents[0].strip()
                time = conversation.select('h4 span')[1].contents[0].strip()
                body = conversation.select('p')[0].contents[0].strip()
                ad_messages.append({
                    'sender': sender,
                    'time': time,
                    'body': body
                })
            unread_messages.append({
                'title': ad_title,
                'url': ad_url,
                'messages': ad_messages
            })
        return unread_messages
