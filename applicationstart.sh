#!/bin/bash

sudo systemctl daemon-reload
sudo systemctl enable gunicorn.socket
sudo systemctl restart gunicorn
sudo systemctl restart nginx