#!/bin/bash
wget https://chromedriver.storage.googleapis.com/2.27/chromedriver_mac64.zip
unzip chromedriver_mac64.zip
rm chromedriver_mac64.zip
chmod +x chromedriver
sudo mv chromedriver /usr/local/bin/chromedrivertest
pip3 install -r requirements.txt
