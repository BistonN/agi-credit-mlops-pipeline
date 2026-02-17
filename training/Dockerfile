FROM rocker/r-ver:4.3.1

WORKDIR /app

COPY packages.R /app/packages.R
RUN Rscript /app/packages.R

COPY train.R /app/train.R

CMD ["Rscript", "train.R"]
