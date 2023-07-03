FROM python:3.9-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Install system dependencies
RUN apt-get update > /dev/null
RUN apt-get install apt-utils gcc build-essential python3-dev libpq-dev libmagic1 curl zip unzip tar gettext -y > /dev/null

# # Install librdkafka (for confluent-kafka-python)
RUN git clone https://github.com/edenhill/librdkafka.git > /dev/null
WORKDIR /librdkafka
RUN ./configure > /dev/null
RUN make > /dev/null
RUN make install > /dev/null

# changing to user
RUN useradd --create-home user
USER user

WORKDIR /home/user/backend

# Python dependencies
ENV PATH /home/user/.local/bin:$PATH
# RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir pipenv
COPY Pipfile Pipfile.lock /home/user/backend/

USER root
RUN chown -R user:user /home/user
# Installing with dev dependencies for development
USER user
RUN pipenv install --dev

# Clean the house
# RUN apt-get purge libpq-dev -y && apt-get autoremove -y
# RUN rm /var/lib/apt/lists/* rm -rf /var/cache/apt/*

COPY . /home/user/backend/