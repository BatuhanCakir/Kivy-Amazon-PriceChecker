from bs4 import BeautifulSoup
import requests
from re import sub
from decimal import Decimal
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

def check(email):
    return re.search(regex, email)




def check_item(url):
    try:
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            return response
        return None

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        return None


def check_price(price1,response):
    soup = BeautifulSoup(response.content, features="lxml")
    title = soup.select("#productTitle")[0].get_text().strip()
    price = soup.select("#priceblock_ourprice")[0].get_text().strip()
    value = Decimal(sub(r'[^\d.]', '', price))
    value2 = Decimal(sub(r'[^\d.]', '', price1) )
    email_msg = "Der Preis von " + title + " ist " + price
    if value <value2:
        return email_msg
    else:
        return None


MY_ADDRESS = "YOUR EMAIL ADDRESS"
PASSWORD = "YOUR EMAIL PASSWORD"
def send_mail(email_msg):
    #You have to configure the smtp server for yourself its now configured for out emails
    s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)
    for email in contacts:
        msg = MIMEMultipart()
        msg['From'] = MY_ADDRESS
        msg['To'] = email
        msg['Subject'] = "amazon Price"
        msg.attach(MIMEText(email_msg, 'plain'))
        s.send_message(msg)
        del msg



contacts =[]
def add_contacts(email):
    contacts.append(email)



import kivy
kivy.require('1.11.1')


from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout


from os import listdir
kv_path = 'untitled1/kv/'
for kv in listdir(kv_path):
    Builder.load_file(kv_path+kv)




class Container(BoxLayout):
    display = ObjectProperty()

    def submit(self,email,url,price):
        response = check_item(url)
        if response != None:
            price_check=check_price(price,response)
            if check(email):
                add_contacts(email)

                while True:
                    if price_check !=None:
                        send_mail(price_check)
                    time.sleep(100)
                    response = check_item(url)
                    price_check = check_price(price, response)
            else :
                self.display.text = 'Not a valid Email'
        else :
            self.display.text = 'No Item with that Url'







class MainApp(App):
    def build(self):
        self.title = 'Awesome app!!!'
        return Container()


if __name__ == "__main__":
    app = MainApp()
    app.run()








