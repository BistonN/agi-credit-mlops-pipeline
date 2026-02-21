FROM rocker/r-ver:4.3.1

WORKDIR /app

RUN apt-get update && apt-get install -y jq

COPY packages.R /app/packages.R
RUN Rscript /app/packages.R

COPY train.R /app/train.R
COPY versioning.sh /app/versioning.sh

RUN chmod +x /app/versioning.sh

CMD Rscript /app/train.R && /app/versioning.sh