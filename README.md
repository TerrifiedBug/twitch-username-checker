# 🐳 Twitch Username Availability Checker (Dockerized)

Check the availability of Twitch usernames on a schedule — complete with optional notifications via **Discord** and **CallMeBot (WhatsApp)**, and full Docker support.

---

## 🧰 Features

- ✅ Headless browser check via Playwright
- ✅ Configurable username list
- ✅ Discord + WhatsApp alerts
- ✅ Optional screenshot saving for debugging purposes
- ✅ Dockerized with cron scheduling
- ✅ Environment-driven configuration

---

## 🚀 Getting Started

### 🐳 1. Clone the Repository

```bash
git clone https://github.com/TerrifiedBug/twitch-username-checker.git
cd twitch-username-checker
```

---

### ⚙️ 2. Configure `.env`

Create a `.env` file:

```env
# Comma-separated list of usernames to check
USERNAMES=

# Cron schedule (twice daily example)
CRON_SCHEDULE=0 8,20 * * *

# Notifications
DISCORD_ENABLED=true
DISCORD_WEBHOOK=https://discord.com/api/webhooks/...

CALLMEBOT_ENABLED=true
CALLMEBOT_PHONE=+441234567890
CALLMEBOT_APIKEY=abcdef123456

# Screenshots
SCREENSHOTS_ENABLED=false
```

---

### 📁 3. Files You Should Have

```
.
├── docker-compose.yml
├── Dockerfile
├── .env.template             # .env template to create your .env from
├── .env                      # Your populated .env file
├── config.json               # Field selectors & UI config
├── twitch_username_check.py  # Main script
├── docker-entrypoint.sh      # Sets up cron
├── requirements.txt          # Requirements
```

---

### 🐳 4. Build and Run

```bash
docker compose build
docker compose up -d
```

📝 Output is logged to `cron-logs/cron.log`

---

## 🔧 Configuration Files

### 📄 `config.json`

Defines the HTML selectors used to fill/check the site. Already configured for [streampog.com](https://streampog.com):

```json
{
  "site": {
    "url": "https://streampog.com/twitch-username-checker",
    "username_field": "input[name=\"username\"]",
    "submit_button": "button[type=\"submit\"]",
    "result_selector": "#result"
  },
  "screenshots": {
    "enabled": false,
    "path_format": "screenshots/debug_{username}.png"
  }
}
```

---

## 🧪 Test Manually Inside Container

```bash
docker exec -it twitch-username-checker bash
python3 twitch_username_check.py
```

---

## 📬 Notifications

| Type        | Config                                  |
|-------------|------------------------------------------|
| Discord     | Enable via `.env` and set webhook URL    |
| CallMeBot   | Enable via `.env`, phone number + API key|

---

## 📅 Cron Schedule Examples

| Schedule            | CRON_SCHEDULE              |
|---------------------|----------------------------|
| Every day at midnight     | `0 0 * * *`              |
| Twice a day (8 AM + 8 PM) | `0 8,20 * * *`        |

Use [crontab.guru](https://crontab.guru) for easy syntax checks.

---

## ⚠️ Disclaimer
This project uses a headless browser to interact with [Streampog](https://streampog.com/twitch-username-checker) to check Twitch username availability.

> **Please use this tool responsibly.**
> This tool relies on Streampog's public Twitch Username Checker. It is not affiliated with or endorsed by Streampog.

> Please use this tool respectfully. It is designed to mimic normal user interaction and should be ran at most twice per day.

> Do not configure cron run it more frequently than necessary, and avoid sending high volumes of automated requests that could disrupt or overload Streampog’s services.


We are not affiliated with Streampog or Twitch. This tool is intended for personal or educational use only.

If you are the owner of Streampog and have concerns about this tool, please [open an issue](https://github.com/TerrifiedBug/twitch-username-checker/issues) or contact the repository maintainer directly at admin@terrifiedbug.com

---

## 🙌 Credits

Built using:

- [Playwright](https://playwright.dev/)
- [Docker](https://docker.com/)
- [Streampog](https://streampog.com/)
