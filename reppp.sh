#!/bin/bash

cd stream_sys
docker compose down
cd ..
rm -r -f stream_sys/
git clone -b lite_version_forbilibili git@github.com:JackyM04/stream_sys.git
cd stream_sys
docker compose up -d --build
cd ..