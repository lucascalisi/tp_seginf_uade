#!/bin/bash
docker build -t pki-api .
docker run -it -p 8080:8080 pki-api 
