# 🐳 Multi-Site Twitch Username Availability Checker (Dockerized)

[![Docker Pulls](https://img.shields.io/docker/pulls/terrifiedbug/twitch-username-checker)](https://hub.docker.com/r/terrifiedbug/twitch-username-checker)

Check the availability of Twitch usernames across multiple sites on a schedule — complete with optional notifications via **Discord**, **CallMeBot (WhatsApp)**, and full Docker support.

---

## 🧰 Features

- ✅ Headless browser check via Playwright
- ✅ Multi-site checking with different methods (direct URL and form-based)
- ✅ Configurable username list
- ✅ Discord + WhatsApp alerts
- ✅ Optional screenshot saving for debugging purposes
- ✅ Dockerized with cron scheduling
- ✅ Environment-driven configuration
- ✅ Modular code structure for easy extension

---

## 🚀 Getting Started

### 🐙 Option 1: Use Prebuilt Image from Docker Hub

#### 1. Create a `.env` file:

```env
# Comma-separated list of usernames to check
USERNAMES=yourname1,yourname2

# Comma-separated list of sites to check (must match config.json keys)
WEBSITES=twitch,streampog

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

## 📁 Project Structure

```
.
├── .env                       # Your environment variables
├── .env.template              # Sample template
├── config.json                # Field selectors & UI config
├── setup.py                   # Python package configuration
├── docker-compose.yml         # Docker Compose setup
├── Dockerfile                 # Docker image builder
├── docker-entrypoint.sh       # Entrypoint for cron setup
├── requirements.txt           # Python dependencies
├── username_checker/          # Python package
│   ├── __init__.py            # Package initialization
│   ├── cli.py                 # CLI entry point
│   ├── config/                # Configuration handling
│   ├── services/              # Core services
│   └── utils/                 # Utilities
├── cron-logs/                 # Log output from cron
└── screenshots/               # Screenshots saved here
```

---

## 🔧 Configuration

### 📄 `config.json`

Defines configuration for each site to check. Currently configured for direct Twitch checking and [streampog.com](https://streampog.com):

```json
{
    "twitch": {
        "type": "direct",
        "url": "https://www.twitch.tv/",
        "error_selector": "[data-a-target=\"core-error-message\"]"
    },
    "streampog": {
        "type": "form",
        "url": "https://streampog.com/twitch-username-checker",
        "username_field": "input[name='username']",
        "submit_button": "button[type='submit']",
        "result_selector": "#result",
        "success_class": "alert-success",
        "success_text": "Username is available!"
    }
}
```

### 📊 Check Types

The tool supports two types of availability checks:

1. **Direct URL** (`type: "direct"`): Navigates to URL + username and checks for an error element
2. **Form-based** (`type: "form"`): Submits username to a form and checks the result

---

## 📬 Notifications

| Type      | Environment Variables Required                      |
|-----------|-----------------------------------------------------|
| Discord   | `DISCORD_ENABLED=true`, `DISCORD_WEBHOOK=...`       |
| CallMeBot | `CALLMEBOT_ENABLED=true`, `CALLMEBOT_PHONE=...`, `CALLMEBOT_APIKEY=...` |

---

## 🧪 Run It Manually (for testing)

```bash
# Using container name:
docker exec -it twitch-username-checker bash
python -m username_checker.cli

# Or if using deprecated approach:
python twitch_username_check.py
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
This project uses a headless browser to interact with external sites like [Streampog](https://streampog.com/twitch-username-checker) to check Twitch username availability.

> **Please use this tool responsibly.**
> This tool relies on public username checking services. It is not affiliated with or endorsed by Streampog or Twitch.

> **Please use this tool respectfully.**
> It is designed to mimic normal user interaction and should be run at most twice per day.

> Do not configure cron to run more frequently than necessary, and avoid sending high volumes of automated requests that could disrupt or overload services.

This tool is intended for personal or educational use only.

If you are the owner of any services used by this tool and have concerns, feel free to [open an issue](https://github.com/TerrifiedBug/twitch-username-checker/issues) or contact the repository maintainer at `admin@terrifiedbug.com`.

---

## 🙌 Credits

Built with ❤️ using:

- [Playwright](https://playwright.dev/)
- [Docker](https://docker.com/)
- [Streampog](https://streampog.com/)
