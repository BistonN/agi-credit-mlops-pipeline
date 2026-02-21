FROM rocker/r-ver:4.3.1

WORKDIR /app

RUN apt-get update && apt-get install -y jq wget

COPY packages.R /app/packages.R
RUN Rscript /app/packages.R

COPY train.R /app/train.R
COPY versioning.sh /app/versioning.sh

RUN chmod +x /app/versioning.sh

RUN mkdir -p /app/data

RUN if [ ! -f /app/data/application_train.csv ]; then \
      wget -O /app/data/application_train.csv "https://www.dropbox.com/scl/fi/hmhnf33bbapvpsq6becmo/application_train.csv?rlkey=t9i95h11b1uyc6dsh6s40z3x4&st=xzu9ijx2&dl=0" && \
      head /app/data/application_train.csv | grep -qi html && exit 1 || true ; \
    fi

CMD Rscript /app/train.R && /app/versioning.sh