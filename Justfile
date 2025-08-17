#!/usr/bin/env just --justfile

run:
  ./server.py -o

build:
  ./build.py

gen-highlight:
  uvx --from pygments pygmentize -S default -f html -a .highlight > highlight.css
