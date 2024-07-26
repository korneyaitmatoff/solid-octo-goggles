FROM ubuntu:22.04

WORKDIR solid_octo_goggles
COPY . ./

RUN apt-get update && apt-get install -y python3
RUN apt-get install -y python3-venv
RUN apt-get install -y python3-pip
RUN apt-get install -y libpq-dev

RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt

RUN playwright install
RUN playwright install-deps