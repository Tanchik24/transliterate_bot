FROM python:slim
COPY . .
RUN pip install --upgrade pip && \
    pip install --ignore-installed  -r ./requirements.txt
CMD python transliterate_bot.py