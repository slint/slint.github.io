#!/usr/bin/env python
from distutils.dir_util import copy_tree
from pathlib import Path
import shutil
import subprocess
from datetime import datetime as dt
from urllib.parse import urlparse

from jinja2 import Template, Markup
import mistune
import pygments
import pygments.lexers
import pygments.formatters.html

print('build started')

output_dir = Path('_build')
output_dir.mkdir(exist_ok=True)

template = Template(Path('base.jinja2').read_text())

class CustomRenderer(mistune.Renderer):

    # override to use pygmentize for code highlighting
    def block_code(self, code, lang):
        if not lang:
            return f'\n<pre><code>{mistune.escape(code)}</code></pre>\n'
        lexer = pygments.lexers.get_lexer_by_name(lang, stripall=True)
        formatter = pygments.formatters.html.HtmlFormatter()
        return pygments.highlight(code, lexer, formatter)

    # override to generate external links that open in a new browser tab
    def link(self, link, title, text):
        link = mistune.escape_link(link)
        target = ''
        if urlparse(link).netloc:
            target = 'target="_blank"'
        if not title:
            return f'<a {target} href="{link}">{text}</a>'
        title = mistune.escape(title, quote=True)
        return f'<a {target} href="{link}" title="{title}">{text}</a>'


md = mistune.Markdown(renderer=CustomRenderer())

def extract_date_info(md_file):
    if 'blog' in md_file.parts:
        try:
            # fetch all modification dates for the file from "git log"
            output = subprocess.check_output(
                f'git log --format=%ai {md_file}', encoding='utf8', shell=True)
            dates = [l.strip() for l in output.splitlines() if l.strip()]
            return (
                # last date is that of creation
                dt.strptime(dates[-1], "%Y-%m-%d %H:%M:%S %z"),
                # first date is from last update
                dt.strptime(dates[0], "%Y-%m-%d %H:%M:%S %z"),
            )
        except Exception:
            pass
    return None, None


def extract_title(markdown):
    # mistune parses Markdown into tokens. First level-1 header is the title
    return next((
        token['text'] for token in mistune.BlockLexer().parse(markdown)
        if token['type'] == 'heading' and token['level'] == 1
    ), None)


def md_to_html(md_path):
    markdown = md_path.read_text()

    created, updated = extract_date_info(md_path)
    title = extract_title(markdown)
    html = md.parse(markdown)
    return title, created, updated, template.render(
        title=title,
        created=created,
        updated=updated,
        content=Markup(html),
    )


blog_posts = []

for md_file in Path('content').glob('**/*.md'):
    print(f'processing {md_file}')
    title, created, updated, html = md_to_html(md_file)
    if 'blog' in md_file.parts:
        blog_posts.append((md_file.stem, title, created, updated))

    output_file = output_dir / Path(*md_file.with_suffix('.html').parts[1:])
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(html)
    print(f'writing {output_file}')

# Build index page
lines = []
for slug, title, created, _ in sorted(blog_posts, key=lambda p: p[2], reverse=True):
    created_str = (created or dt.now()).strftime("%A, %B %-d, %Y")
    lines.append(f'- [{title}](/blog/{slug}.html) ({created_str})')

output_file = output_dir / 'index.html'
output_file.write_text(template.render(
    content=Markup(md.parse('\n'.join(lines)))
))

# Copy CSS files
shutil.copy('style.css', output_dir)
shutil.copy('highlight.css', output_dir)

# Copy images
copy_tree('content/images', str(output_dir / 'images'))

print('build finished')
