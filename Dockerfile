# Pull base image
FROM python:3.7
# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /web/
# Install dependencies
RUN pip install pipenv
COPY Pipfile /web/
COPY Pipfile.lock /web/
RUN pipenv install --system --dev
RUN pip install selenium==4.6.0
RUN pip install webdriver-manager
RUN pip install alembic
COPY . /web/
EXPOSE 8000
CMD ["python", "web/main.py"]
