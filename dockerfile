FROM python:slim
COPY . .
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt
CMD python transliterate_bot.py