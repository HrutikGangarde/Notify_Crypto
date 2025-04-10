import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Define your email credentials
EMAIL_ADDRESS = 'hrutik@teesta.co'
EMAIL_PASSWORD = 'pnti ymta rumh encl'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465

# Define the recipient email address
RECIPIENT_EMAIL = 'recipient_email@example.com'

# Define the cryptocurrencies and their threshold prices
thresholds = {
    'bitcoin': 80000,    # Alert if Bitcoin falls below $45,000
    'ethereum': 1400 ,    # Alert if Ethereum falls below $3,000
    'ripple': 1.0     # Alert if Ripple falls below $0.45
}

def get_crypto_prices(crypto_ids):
    """
    Fetches the current USD prices for the specified cryptocurrencies from CoinGecko API.
    """
    ids = ','.join(crypto_ids)
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data from CoinGecko: {response.status_code}")
        return None

def send_email_notification(subject, body, to_email):
    """
    Sends an email notification with the given subject and body to the specified email address.
    """
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        print(f"Email sent to {to_email} with subject: {subject}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def main():
    crypto_ids = list(thresholds.keys())
    prices = get_crypto_prices(crypto_ids)

    if prices:
        for crypto_id, threshold in thresholds.items():
            current_price = prices.get(crypto_id, {}).get('usd')
            if current_price is not None:
                print(f"The current price of {crypto_id.capitalize()} is ${current_price}")
                if current_price < threshold:
                    subject = f"{crypto_id.capitalize()} Price Alert"
                    body = (f"The price of {crypto_id.capitalize()} has fallen below ${threshold}.\n"
                            f"Current price: ${current_price}")
                    send_email_notification(subject, body, RECIPIENT_EMAIL)
            else:
                print(f"Price data for {crypto_id} is not available.")
    else:
        print("Failed to fetch price data.")

if __name__ == "__main__":
    main()

