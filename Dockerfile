FROM python:3.12-alpine
WORKDIR /app
ENV PYTHONUNBUFFERED=1 PORT=3000
COPY bot.py .
RUN adduser -D bot
USER bot
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s CMD wget -qO- http://127.0.0.1:${PORT}/health || exit 1
CMD ["python", "bot.py"]
