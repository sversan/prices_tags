import smtplib, ssl
import pandas as pd
import requests
from bs4 import BeautifulSoup
from price_parser import Price
import gnupg
import getpass
from pathlib import Path
import maskpass 

PRODUCT_URL_CSV = "product_urls.csv"
SAVE_TO_CSV = True
PRICES_CSV = "prices.csv"
SEND_MAIL = True
#passwd = getpass.getpass(prompt="Type your password and press enter: ", forcemask=True)
pwd = maskpass.askpass(prompt="Type your password and press enter: ")

def get_urls(csv_file_path):
    df = pd.read_csv(csv_file_path)
    return df

def process_products(df):
    for product_url in df.to_dict('records'):
        df.updated.to_csv(PRICES_CSV, mode="a")

def get_response(url):
    response = requests.get(url)
    return response.text

def get_price(html):
    soup = BeautifulSoup(html, "lxml")  
    el = soup.select_one(".price_color")
    price = price.fromstring(el.text)
    return price.amount_float

def process_products(df):
    updated_products = []
    for product in df.to_dict("records"):
        html = get_response(product["url"])
        product["price"] = get_price(html)
        product["alert'"] = product["price"] <= product["alert.price"]
        updated_products.append(product)
    return pd.DataFrame(updated_products)

    if SAVE_TO_CSV:
        df.updated.to_csv(PRICES_CSV, mode="a")

    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "stefanversan@gmail.com"
    password = pwd

# Create a secure SSL context
    context = ssl.create_default_context()


    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        # TODO: Send email here
    except Exception as e:
        print("Error while sending email!") 
    finally:
        server.quit()

def main():
    df = get_urls(PRODUCT_URL_CSV)
    df_updated = process_products(df)
    if SAVE_TO_CSV:
        df_updated.to_csv(PRICES_CSV, mode="a", index=False)
    if SEND_MAIL == True:
        df_updated.to_csv(PRICES_CSV, mode="a", index=True)

    if __name__ == "__main__":
        main()























    
    

