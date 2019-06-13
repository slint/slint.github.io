#!/usr/bin/env python
from livereload import Server, shell
import subprocess

# run initial build
subprocess.run('./build.py')

server = Server()
server.watch('base.jinja2', './build.py')
server.watch('content/*.md', './build.py')
server.watch('content/blog/*.md', './build.py')
server.watch('*.css', './build.py')
server.serve(root='_build/')
