docker build -t elif2/elasticsearch-dev -f docker/Dockerfile.elasticsearch .
docker run -d --name elasticsearch_dev -p 9200:9200 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  elif2/elasticsearch-dev

# or just
docker-compose down -v                             
docker-compose up --build