#!/usr/bin/env python
from livereload import Server, shell
import subprocess
import sys

# run initial build
subprocess.run('./build.py')

server = Server()
server.watch('base.jinja2', './build.py')
server.watch('content/*.md', './build.py')
server.watch('content/blog/*.md', './build.py')
server.watch('*.css', './build.py')

open_in_browser = '-o' in sys.argv
server.serve(root='_build/', open_url=open_in_browser)
