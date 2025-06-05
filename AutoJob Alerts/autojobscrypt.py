import logging
import requests
from bs4 import BeautifulSoup
import time
import random
import schedule
from flask import session
from tenacity import retry,stop_after_attempt,wait_fixed
from dotenv import load_dotenv
import os
load_dotenv()
telegram_token = os.getenv('telegram_token')
telegram_chat_id = os.getenv('telegram_chat_id')
logging.basicConfig(filename="job_finder.log",level=logging.INFO)
#function to scrap the available jobs
@retry(stop=stop_after_attempt(3),wait=wait_fixed(2))
def scrap_jobs():
    try:
        time.sleep(random.uniform(2, 5))  # 2 to 5 seconds between requests
        url = 'https://remoteok.com/remote-dev-jobs'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        time.sleep(random.uniform(5, 15))  # longer delay
        session_request=requests.Session()
        response = session_request.get(url,headers=headers)
        response.raise_for_status()
        data = response.text
        soup = BeautifulSoup(data, "lxml")
        jobs = soup.find_all("tr", class_="job")
        available_jobs = []
        logging.info(f'Found {len(jobs)} jobs')
        print(f'Found {len(jobs)} jobs')
        for job in jobs:
            title = job.find("h2", itemprop="title").text.strip()

            employer = job.find("h3", itemprop="name")
            employer = employer.text.strip() if employer else "N/A"
            locations = job.find_all("div", class_="location")
            salary = locations[0].text.strip() if len(locations) > 0 else "N/A"
            job_location = locations[1].text.strip() if len(locations) > 1 else "N/A"
            time_tag = job.find('time')
            time_past = time_tag.get_text(strip=True) if time_tag else "N/A"
            link_tag=job.find("a",class_="preventLink")
            link=link_tag['href'] if link_tag else '#'
            full_link='https://weworkremotely.com' + link if link.startswith('/') else link

            available_jobs.append({
                "Title": title,
                "Location": job_location,
                "Employer": employer,
                "Salary range": salary,
                "Time posted": time_tag,
                "Time past": time_past,
                "Link":full_link
            })
        return available_jobs
    except Exception as error:
        logging.error(f"An error,{error} occurred")
        print(f"An error,{error} occurred")



def send_telegram_message(jobs):
    token = telegram_token
    chat_id = telegram_chat_id
    if not jobs:
        text = "No jobs found 😞, or code failed to scrap available jobs"
    else:
        text = "🚀 *Latest Remote Dev Jobs:*\n\n"
        for job in jobs[:5]:
            text += (
                f"*{job['Title']}* at *{job['Employer']}*\n"
                f"📍 _{job['Location']}_ | 💰 _{job['Salary range']}_\n"
                f"🕒 Posted: _{job['Time past']}_\n"
                f"🔗 [Apply here]({job['Link']})\n\n"
            )

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode":"Markdown"
    }
    try:
        res = requests.post(url, data=payload)
        res.raise_for_status()
        print("✅ Message sent to Telegram" )
    except Exception as e:
        print(f"❌ Failed to send Telegram message: {e}")

def job_task():
    jobs = scrap_jobs()
    send_telegram_message(jobs)
job_task()#checks if the code is working properly(not required in this code though)
if __name__ == "__main__":
    schedule.every().day.at("10:00").do(job_task)
    print("Scheduler is running...")
while True:
    schedule.run_pending()
    time.sleep(60)