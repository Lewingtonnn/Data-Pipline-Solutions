🏘 Real Estate Listing Scraper & Alert System
This Python automation project scrapes property listings from Craigslist (or similar real estate platforms), filters out key details (like title, price, location, and bedrooms), and sends real-time alerts to users via Telegram and email.

🔧 Features
✅ Scrapes latest property listings with BeautifulSoup

✅ Extracts title, price, location, number of bedrooms, and listing link

✅ Sends alerts to Telegram using bots with rich formatting

✅ Sends HTML-formatted property summaries via email

✅ Saves data to a CSV for record-keeping

✅ Uses .env for environment variables (no hard-coded secrets)

✅ Includes logging and retry handling with tenacity for robustness

📦 Tech Stack
Python

requests, BeautifulSoup, pandas

smtplib & email.mime for sending email

tenacity for retries

python-dotenv for managing secrets

Telegram Bot API

📸 Sample Output (Telegram)


🏘️ New Property Listings

🏠 Beautiful 2-Bed Apartment
💵 $1200 | 🛏️ 2 Beds
📍 Brooklyn, NY
🔗 View Listing

Built by Lewis Ng'ang'a (https://github.com/Lewingtonnn)