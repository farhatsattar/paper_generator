#!/bin/bash
sudo apt-get update
sudo apt-get install -y fonts-noto fonts-noto-cjk fonts-noto-color-emoji fonts-noto-ui-core
fc-cache -fv  # Refresh font cache
