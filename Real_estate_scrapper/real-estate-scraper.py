import logging
import os
import smtplib
import requests
import pandas as pd
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_fixed

# Configure logging
logging.basicConfig(
    filename="real_estate_scraper.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
CONFIG = {
    'telegram_token': os.getenv('TELEGRAM_TOKEN'),
    'telegram_chat_id': os.getenv('TELEGRAM_CHAT_ID'),
    'email_user': os.getenv('EMAIL_USER'),
    'email_password': os.getenv('EMAIL_PASSWORD'),
    'email_receiver': os.getenv('EMAIL_RECEIVER')
}


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def scrape_properties(url: str) -> list[dict]:
    """Scrape property listings from target URL.

    Args:
        url: URL to scrape property data from

    Returns:
        List of dictionaries containing property data
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        listings = soup.find_all('li', class_='cl-static-search-result') or \
                   soup.find_all('div', class_='result-row') or \
                   soup.find_all('div', class_='cl-search-result')

        logger.info(f"Found {len(listings)} properties")
        print(f"Found {len(listings)} properties")

        properties = []
        for listing in listings:
            try:
                title = listing.find('div', class_='title').text.strip() if listing.find('div',
                                                                                         class_='title') else "N/A"
                price = listing.find('div', class_='price').text.strip() if listing.find('div',
                                                                                         class_='price') else "N/A"
                location = listing.find('div', class_='location').text.strip() if listing.find('div',
                                                                                               class_='location') else "N/A"
                bedrooms = listing.find('span', class_='housing') or listing.find('span', class_='bedrooms')
                bedrooms = bedrooms.text.strip() if bedrooms else "N/A"

                link = listing.find('a', href=True)
                if link:
                    link = link['href']
                    if not link.startswith('http'):
                        link = url + link

                properties.append({
                    "Title": title,
                    "Price": price,
                    "Location": location,
                    "Bedrooms": bedrooms,
                    "Link": link
                })
            except Exception as e:
                logger.warning(f"Error processing listing: {str(e)}")
                continue

        return properties

    except Exception as e:
        logger.error(f"Scraping failed: {str(e)}")
        raise


def save_to_csv(data: list[dict], filename: str = "properties.csv") -> None:
    """Save scraped data to CSV file.

    Args:
        data: List of property dictionaries
        filename: Output filename
    """
    try:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        logger.info(f"Successfully saved {len(df)} listings to {filename}")
        print(f"Saved {len(df)} properties to {filename}")
    except Exception as e:
        logger.error(f"Failed to save CSV: {str(e)}")
        raise


def send_email(data: list[dict]) -> None:
    """Send property listings via email.

    Args:
        data: List of property dictionaries to send
    """
    try:
        msg = MIMEMultipart()
        msg['Subject'] = "🚀 New Property Listings"
        msg['From'] = CONFIG['email_user']
        msg['To'] = CONFIG['email_receiver']

        # Create HTML email content
        html = """<html><body><h2>New Property Listings</h2><table border="1">"""
        html += "<tr><th>Title</th><th>Price</th><th>Bedrooms</th><th>Location</th></tr>"

        for prop in data[:10]:  # Limit to top 10
            html += f"""
            <tr>
                <td><a href="{prop['Link']}">{prop['Title']}</a></td>
                <td>{prop['Price']}</td>
                <td>{prop['Bedrooms']}</td>
                <td>{prop['Location']}</td>
            </tr>"""

        html += "</table></body></html>"

        msg.attach(MIMEText(html, 'html'))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(CONFIG['email_user'], CONFIG['email_password'])
            server.send_message(msg)

        logger.info("Email sent successfully")
        print("Email sent successfully")

    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        raise


def send_telegram_alert(data: list[dict]) -> None:
    """Send property alerts to Telegram.

    Args:
        data: List of property dictionaries to send
    """
    if not data:
        message = "⚠️ No properties found today"
    else:
        message = "🏘️ <b>New Property Listings</b>\n\n"
        for prop in data[:5]:  # Limit to top 5
            message += (
                f"🏠 <b>{prop['Title']}</b>\n"
                f"💵 {prop['Price']} | 🛏️ {prop['Bedrooms']}\n"
                f"📍 {prop['Location']}\n"
                f"🔗 <a href='{prop['Link']}'>View Listing</a>\n\n"
            )

    payload = {
        'chat_id': CONFIG['telegram_chat_id'],
        'text': message,
        'parse_mode': 'HTML',
        'disable_web_page_preview': True
    }

    try:
        response = requests.post(
            f"https://api.telegram.org/bot{CONFIG['telegram_token']}/sendMessage",
            json=payload
        )
        response.raise_for_status()
        logger.info("Telegram alert sent")
        print("Telegram alert sent")
    except Exception as e:
        logger.error(f"Failed to send Telegram alert: {str(e)}")
        raise


def main():
    """Main execution function."""
    try:
        # Target URL - can be parameterized
        target_url = "https://dallas.craigslist.org/search/rea"

        # Scrape properties
        properties = scrape_properties(target_url)

        if properties:
            # Save data
            save_to_csv(properties)

            # Send alerts
            #send_email(properties)-once the emails and passwords are set
            send_telegram_alert(properties)
        else:
            logger.warning("No properties scraped")

    except Exception as e:
        logger.error(f"Script failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()