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

Edit `handle()` in `bot.py` (and `START_TEXT`) to make it your own. Note: on Weblines, only the
one-click **Telegram bot** card runs on the Germany node. An app you create from your own repo runs
in Iran and cannot reach Telegram, so for your own bot code open a ticket.
Guide: https://docs.weblines.ir/apps/telegram-bot

---

**فارسی:** یک ربات تلگرام نمونه: `/start` خوش‌آمد می‌گوید و هر متن دیگری را برمی‌گرداند. در وب‌لاینز از کارت «ربات تلگرام» ساخته می‌شود و روی سرور آلمان اجرا می‌شود، چون تلگرام از ایران در دسترس نیست. اپی که از ریپوی خودتان بسازید روی سرور ایران اجرا می‌شود و به تلگرام وصل نمی‌شود؛ برای ربات با کد خودتان تیکت بزنید. راهنما: https://docs.weblines.ir/apps/telegram-bot
