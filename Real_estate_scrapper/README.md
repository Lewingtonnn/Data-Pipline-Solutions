# 🏘️ Real Estate Listing Scraper & Alert System

A Python automation tool that scrapes real-estate listings from Craigslist, saves them to CSV, and sends rich alerts via **Telegram** and **Email**.

---

## 📌 Features

- 🔍 Scrapes the newest property listings from a target Craigslist URL  
- 📄 Extracts: **Title, Price, Location, Bedrooms, Link**  
- 💬 Sends formatted Telegram messages (HTML mode)  
- 📧 Emails an HTML table with up to 10 listings  
- 🗂 Persists all listings to `properties.csv`  
- 🔁 Robust retry logic with **tenacity**  
- 🔐 Secrets managed through `.env`

---

## ⚙️ Tech Stack

| Purpose            | Libraries / Tools |
|--------------------|-------------------|
| Web scraping       | `requests`, `beautifulsoup4` |
| Data handling      | `pandas` |
| Email alerts       | `smtplib`, `email.mime` |
| Telegram alerts    | **Telegram Bot API** |
| Retry / resilience | `tenacity` |
| Secret management  | `python-dotenv` |
| Language           | **Python 3.10+** |

---

## 🛠 How It Works

1. **Scrape** – grabs all listing blocks from the city’s Craigslist search page.  
2. **Parse & format** – pulls out title, price, location, bedrooms, link.  
3. **Alert users** – top 5 to Telegram, top 10 to email.  
4. **Persist** – appends every scrape run to `properties.csv` (handy for analysis).

---

## 🔐 Environment Setup

Create a `.env` file in the project root:

```dotenv
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECEIVER=receiver_email@gmail.com
```
### ▶️ How to Run

python main.py

**Once executed, the script will:**

1. Scrape listings from Craigslist (Dallas area by default)

2. Save them to properties.csv

3. Send top results to your Telegram and email inbox

## 🧾 Example Output

### 📧 Email Output

| Title            | Price  | Bedrooms | Location    |
|------------------|--------|----------|-------------|
| Cozy 2-Bed       | $1200  | 2 Beds   | Uptown      |
| Modern Loft      | $1450  | 1 Bed    | Deep Ellum  |
| Spacious Studio  | $900   | Studio   | Downtown    |

---

### 📬 Telegram Message Example

🏘️ **New Property Listings**

🏠 **Cozy 2-Bed in Dallas**  
💵 $1,200 | 🛏️ 2 Beds  
📍 Uptown, Dallas  
🔗 [View Listing](https://dallas.craigslist.org/example1)

🏠 **Modern Loft**  
💵 $1,450 | 🛏️ 1 Bed  
📍 Deep Ellum  
🔗 [View Listing](https://dallas.craigslist.org/example2)

---

## 🚀 Future Improvements

- Add filtering options (e.g., price range, bedrooms, keywords) for more customized alerts  
- Support scraping and alerts for multiple cities beyond Dallas  
- Integrate exporting data to Google Sheets for easy sharing and collaboration  
- Add Slack alert notifications for workplace integration  
- Containerize with Docker and deploy with GitHub Actions for automated runs  

Deployment via GitHub Actions / Docker

# 👤 Author
## **Lewis Ng'ang'a**
### **Python Automation Enthusiast**
## GitHub: @Lewingtonnn


