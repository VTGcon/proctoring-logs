FROM python:3
RUN mkdir zxc
COPY . /zxc/
WORKDIR /zxc
RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
RUN pip install --upgrade pip
RUN pip install --user -r requirements.txt
CMD [ "python", "runner.py", "--help" ]
