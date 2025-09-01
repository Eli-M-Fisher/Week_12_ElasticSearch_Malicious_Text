docker build -t elif2/elastic-api -f docker/Dockerfile.api .
docker run -d --name elastic_api -p 8000:8000 \
  --link elasticsearch_dev:elasticsearch \
  elif2/elastic-api