#!/bin/bash
docker build -t pki-api .
docker run -v app:/opt/ca_manager/app -it -p 8080:8080 pki-api 
