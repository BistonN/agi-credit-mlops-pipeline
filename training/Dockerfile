FROM rocker/r-ver:4.3.1

WORKDIR /app

RUN R -e "install.packages(c('tidymodels','readr','jsonlite'), repos='https://cloud.r-project.org')"

COPY train.R /app/train.R

CMD ["Rscript", "train.R"]
