#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "Jinja2>=3.0.0",
#   "mistune>=3.0.0",
#   "Pygments>=2.10.0",
# ]
# ///
import argparse
import shutil
import subprocess
from datetime import datetime as dt
from datetime import timezone as tz
from pathlib import Path
from urllib.parse import urlparse

import mistune
import pygments
import pygments.formatters.html
import pygments.lexers
from jinja2 import Template
from markupsafe import Markup

print("build started")

# Parse command line arguments
parser = argparse.ArgumentParser(description="Build the static blog")
parser.add_argument(
    "--base-url",
    default="http://127.0.0.1:5500",
    help="Base URL for the site (default: http://127.0.0.1:5500)",
)
args = parser.parse_args()

BASE_URL = args.base_url

output_dir = Path("_build")
output_dir.mkdir(exist_ok=True)

template = Template(Path("base.jinja2").read_text())
template.globals["SITE_BASE_URL"] = BASE_URL


class CustomRenderer(mistune.HTMLRenderer):
    def block_code(self, code, info=None):
        if info is None:
            info = ""
        lang = info.strip()
        if not lang:
            return f"\n<pre><code>{mistune.escape(code)}</code></pre>\n"
        try:
            lexer = pygments.lexers.get_lexer_by_name(lang, stripall=True)
            formatter = pygments.formatters.html.HtmlFormatter()
            return pygments.highlight(code, lexer, formatter)
        except Exception:
            return f"\n<pre><code>{mistune.escape(code)}</code></pre>\n"

    def link(self, text, url, title=None):
        url = mistune.escape_url(url)
        target = ""
        if urlparse(url).netloc:
            target = 'target="_blank"'
        if not title:
            return f'<a {target} href="{url}">{text}</a>'
        title = mistune.escape(title, quote=True)
        return f'<a {target} href="{url}" title="{title}">{text}</a>'


md = mistune.create_markdown(
    renderer=CustomRenderer(), plugins=["strikethrough", "table", "url", "task_lists"]
)


def extract_date_info(md_file: Path):
    if "blog" in md_file.parts:
        try:
            # fetch all modification dates for the file from "git log"
            output = subprocess.check_output(
                f"git log --format=%ai {md_file}", encoding="utf8", shell=True
            )
            dates = [l.strip() for l in output.splitlines() if l.strip()]
            return (
                # last date is that of creation
                dt.strptime(dates[-1], "%Y-%m-%d %H:%M:%S %z"),
                # first date is from last update
                dt.strptime(dates[0], "%Y-%m-%d %H:%M:%S %z"),
            )
        except Exception:
            file_stat = md_file.stat()
            created = dt.fromtimestamp(file_stat.st_ctime, tz=tz.utc)
            updated = dt.fromtimestamp(file_stat.st_mtime, tz=tz.utc)
            return created, updated
    return None, None


def extract_title(markdown):
    # Extract title from first level-1 header
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    return None


def md_to_html(md_path: Path):
    markdown = md_path.read_text()

    created, updated = extract_date_info(md_path)
    title = extract_title(markdown)
    html = md(markdown)

    # Generate the URL for this page
    relative_path = Path(*md_path.with_suffix(".html").parts[1:])
    page_url = f"{BASE_URL}/{relative_path}"

    return (
        title,
        created,
        updated,
        template.render(
            title=title,
            created=created,
            updated=updated,
            content=Markup(html),
            url=page_url,
        ),
    )


blog_posts = []

for md_file in Path("content").glob("**/*.md"):
    print(f"processing {md_file}")
    title, created, updated, html = md_to_html(md_file)
    if "blog" in md_file.parts:
        blog_posts.append((md_file.stem, title, created, updated))

    output_file = output_dir / Path(*md_file.with_suffix(".html").parts[1:])
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(html)
    print(f"writing {output_file}")

# Build index page
lines = []
for slug, title, created, _ in sorted(
    blog_posts,
    key=lambda p: p[2] or dt.now(),
    reverse=True,
):
    created_str = (created or dt.now()).strftime("%A, %B %-d, %Y")
    lines.append(f"- [{title}](/blog/{slug}.html) ({created_str})")

output_file = output_dir / "index.html"
output_file.write_text(template.render(content=Markup(md("\n".join(lines)))))

# Copy CSS files
shutil.copy("style.css", output_dir)
shutil.copy("highlight.css", output_dir)

# Copy images
shutil.copytree("content/images", output_dir / "images", dirs_exist_ok=True)

print("build finished")
