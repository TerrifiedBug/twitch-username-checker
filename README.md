# 🐳 Twitch Username Availability Checker (Dockerized)

[![Docker Pulls](https://img.shields.io/docker/pulls/terrifiedbug/twitch-username-checker)](https://hub.docker.com/r/terrifiedbug/twitch-username-checker)

Check the availability of Twitch usernames...

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

### 🐙 Option 1: Use Prebuilt Image from Docker Hub

#### 1. Create a `.env` file:

```env
# Comma-separated list of usernames to check
USERNAMES=yourname1,yourname2

# Cron schedule (e.g. 8 AM and 8 PM daily)
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

#### 2. Create `docker-compose.yml`:

```yaml
version: "3.9"

services:
  twitch-checker:
    container_name: twitch-username-checker
    image: terrifiedbug/twitch-username-checker:latest
    restart: unless-stopped
    env_file:
      - .env
    working_dir: /app
    volumes:
      - ./cron-logs:/var/log
      - ./screenshots:/app/screenshots
```

#### 3. Run it:

```bash
docker compose pull
docker compose up -d
```

---

### 🛠️ Option 2: Build Image Locally from Dockerfile

#### 1. Clone the Repository:

```bash
git clone https://github.com/TerrifiedBug/twitch-username-checker.git
cd twitch-username-checker
```

#### 2. Configure `.env` (as above)

#### 3. Build & Run Locally:

```bash
docker compose build
docker compose up -d
```

---

## 📁 Files You Should Have

```
.
├── .env                      # Your environment variables
├── .env.template             # Sample template
├── config.json               # Field selectors & UI config
├── twitch_username_check.py  # Main script
├── docker-compose.yml        # Docker Compose setup
├── Dockerfile                # Docker image builder
├── docker-entrypoint.sh      # Entrypoint for cron setup
├── requirements.txt          # Python deps
├── cron-logs/                # Log output from cron
├── screenshots/              # Screenshots saved here
```

---

## 🔧 Configuration

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

## 📬 Notifications

| Type      | Environment Variables Required                      |
|-----------|-----------------------------------------------------|
| Discord   | `DISCORD_ENABLED=true`, `DISCORD_WEBHOOK=...`       |
| CallMeBot | `CALLMEBOT_ENABLED=true`, `CALLMEBOT_PHONE=...`, `CALLMEBOT_APIKEY=...` |

---

## 🧪 Run It Manually (for testing)

```bash
docker exec -it twitch-username-checker bash
python3 twitch_username_check.py
```

---

## 📅 Cron Schedule Examples

| Goal                      | Example Schedule      |
|---------------------------|-----------------------|
| Once a day at midnight    | `0 0 * * *`           |
| Twice a day (8 AM, 8 PM)  | `0 8,20 * * *`        |

Use [crontab.guru](https://crontab.guru) to generate your own.

---

## ⚠️ Disclaimer
This project uses a headless browser to interact with [Streampog](https://streampog.com/twitch-username-checker) to check Twitch username availability.

> **Please use this tool responsibly.**
> This tool relies on Streampog's public Twitch Username Checker. It is not affiliated with or endorsed by Streampog.

> **Please use this tool respectfully.**
> It is designed to mimic normal user interaction and should be ran at most twice per day.

> Do not configure cron run more frequently than necessary, and avoid sending high volumes of automated requests that could disrupt or overload Streampog’s services.

We are not affiliated with Streampog or Twitch. This tool is intended for personal or educational use only.

If you are the owner of Streampog and have any concerns, feel free to [open an issue](https://github.com/TerrifiedBug/twitch-username-checker/issues) or contact the repository maintainer at `admin@terrifiedbug.com`.

---

## 🙌 Credits

Built with ❤️ using:

- [Playwright](https://playwright.dev/)
- [Docker](https://docker.com/)
- [Streampog](https://streampog.com/)
