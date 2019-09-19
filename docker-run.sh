#!/bin/bash
docker build -t pki-api .
docker run -d -v $(pwd)/app/CA_files:/app/CA_files -it -p 8080:8080 pki-api 
