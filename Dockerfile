FROM python:3.7.2-slim
ADD . trainRouting
RUN cd trainRouting && pip3 install -r requirements.txt
ENV FLASK_APP=main.py
EXPOSE 5000
ENTRYPOINT cd trainRouting && flask run -h 0.0.0.0 -p 5000
