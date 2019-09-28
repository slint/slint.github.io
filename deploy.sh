#!/bin/bash

# Build everything
rm -rf _build
./build.py
git checkout master
git pull master

# Move built things in root directory
rsync -r _build/* ./
git add .
git commit -m "$(git log -1 source --format='%h') build"
git push origin master

# go back to dev branch
git checkout source
