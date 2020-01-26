#!/bin/bash

git clone https://github.com/drainware/ddi.git

# Fetch analyzefile repo
cd ddi/
git submodule init
git submodule update

# Create directory for compiled templates
mkdir ddi/templates_c/
chmod -R 777 ddi/templates_c/ 
cd ..

