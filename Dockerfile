FROM python:3.11.4-slim-buster
RUN apt-get update \
 && apt-get install -y gcc

WORKDIR /code

COPY ./pyproject.toml .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir setuptools wheel

COPY . .

RUN pip install --no-cache-dir pyproject.toml \
    && pip install -e .

#COPY ./app /code/app

CMD ["uvicorn", "--factory", "src.project.main:main", "--host", "0.0.0.0", "--port", "8000"]