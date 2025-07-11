FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install -r req.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]