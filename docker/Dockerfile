FROM debian:buster-slim

RUN apt-get update
RUN apt-get install -y --no-install-recommends make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
RUN apt-get install -y tox
ENV HOME="/root"
WORKDIR ${HOME}
RUN apt-get install -y git
RUN git clone --depth=1 https://github.com/pyenv/pyenv.git .pyenv
ENV PYENV_ROOT="${HOME}/.pyenv"
ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${PATH}"

RUN pyenv install 3.6.6
RUN pyenv global 3.6.6

RUN pyenv install 3.7.0
RUN pyenv global 3.7.0

RUN pyenv install 3.8.0
RUN pyenv global 3.8.0

RUN pyenv install 3.9.0
RUN pyenv global 3.9.0

RUN pyenv install 3.10.0
RUN pyenv global 3.10.0

ENV PGDATABASE='postgres'
ENV PGHOST='psql'
ENV PGUSER='postgres'
ENV PGPASSWORD=''

ENV MYSQL_PASSWORD='test'
ENV MYSQL_HOST='mysql'
ENV MYSQL_USER='mysql'

WORKDIR /django-relativedelta
