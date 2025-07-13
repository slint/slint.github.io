#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "livereload==2.6.1",
# ]
# ///
import subprocess
import sys

from livereload import Server

# run initial build
subprocess.run("./build.py")

server = Server()
server.watch("base.jinja2", "./build.py")
server.watch("content/*.md", "./build.py")
server.watch("content/blog/*.md", "./build.py")
server.watch("*.css", "./build.py")

open_in_browser = "-o" in sys.argv
server.serve(root="_build/", open_url_delay=open_in_browser)
