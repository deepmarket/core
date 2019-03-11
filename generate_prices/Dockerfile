FROM python:3.6.8-stretch

RUN mkdir -p /core/generate

WORKDIR /core/generate

COPY . /core/generate

RUN python -m pip install -r requirements.txt

ENV API_PRICING_ENDPOINT=http://pacific.cs.pdx.edu/api/v1/pricing

CMD [ "python", "main.py" ]
