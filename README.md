# Telegram bot — Weblines starter

A minimal Telegram bot: `/start` greets, everything else is echoed back.
Long polling, so it needs no public URL or webhook. Python standard library only.

- `TELEGRAM_BOT_TOKEN` — from [@BotFather](https://t.me/BotFather) (`/newbot`).
- `PORT` — health endpoint port, default `3000` (`GET /health`).

Deploy on Weblines: dashboard → **Telegram bot** → paste the token.
Runs on our Germany node, since Telegram is not reachable from Iran.

Run locally:

```bash
docker build -t tg-bot . && docker run -e TELEGRAM_BOT_TOKEN=... -p 3000:3000 tg-bot
```

Edit `handle()` in `bot.py` to make it your own.
