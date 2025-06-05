# AutoJob Alerts 🚀

A Python automation bot that scrapes remote developer jobs from [RemoteOK](https://remoteok.com/remote-dev-jobs) and sends top listings to Telegram daily.

## Features
- Scrapes job title, employer, location, salary, and posting time
- Sends daily job alerts to your Telegram
- Retries on network errors using `tenacity`
- Scheduled with `schedule`
- Logs activity to `job_finder.log`

## Setup
1. Clone the repo.
2. Add a `.env` file with your Telegram bot token and chat ID:
3. Install dependencies:
```bash
pip install -r requirements.txt
Run:
python.main.py