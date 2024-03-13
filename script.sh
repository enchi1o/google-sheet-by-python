#!/bin/bash

printenv | grep -v "no_proxy" >> /etc/environment &
gunicorn -w 1 --timeout 600 -b 0.0.0.0:8080 main:app