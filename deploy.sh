docker build -t ocr-api .
docker run -p 8000:8000 --network local_network --name ocr-api ocr-api