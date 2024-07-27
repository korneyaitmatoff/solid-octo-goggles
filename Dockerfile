FROM python:3.10-slim

WORKDIR solid_octo_goggles

COPY . ./

RUN apt-get update && apt-get install -y libpq-dev

RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install && playwright install-deps

CMD ["uvicorn", "app:app"]