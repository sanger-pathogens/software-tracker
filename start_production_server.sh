#!/bin/bash
sudo gunicorn3 -w 4 -b 0.0.0.0:80 api:app