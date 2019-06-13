#!/usr/bin/env python
from pathlib import Path
import shutil
import subprocess
from datetime import datetime
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

    def block_code(self, code, lang):
        if not lang:
            return f'\n<pre><code>{mistune.escape(code)}</code></pre>\n'
        lexer = pygments.lexers.get_lexer_by_name(lang, stripall=True)
        formatter = pygments.formatters.html.HtmlFormatter()
        return pygments.highlight(code, lexer, formatter)

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

def extract_date_info(file):
    try:
        output = subprocess.check_output(f'git log --format=%ai {file}')
        dates = [l.strip() for l in output.splitlines() if l.strip()]
        if dates:
            return (
                # created
                datetime.strptime(dates[-1], "%Y-%m-%d %H:%M:%S %z"),
                # updated
                datetime.strptime(dates[0], "%Y-%m-%d %H:%M:%S %z"),
            )
    except Exception:
        pass
    return datetime.now(), datetime.now()

def md_to_html(md_file):
    created, updated = None, None
    if 'blog/' in str(md_file):
        created, updated = extract_date_info(md_file)
    content = md_file.read_text()
    parsed = mistune.BlockLexer().parse(content)[0]
    title = parsed['text'] if parsed['type'] == 'heading' and parsed['level'] == 1 else None
    html = md.parse(content)
    return title, created, updated, template.render(
        title=title,
        created=created,
        updated=updated,
        content=Markup(html),
    )

all_posts = []

for content_file in Path('content').glob('**/*.md'):
    print(f'processing {content_file}')
    title, created, updated, html = md_to_html(content_file)
    if 'blog' in content_file.parts:
        all_posts.append((content_file.stem, title, created, updated))
    output_file = output_dir / Path(*content_file.with_suffix('.html').parts[1:])
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(html)
    print(f'writing {output_file}')

# Build index page
lines = []
for slug, title, created, _ in sorted(all_posts, key=lambda p: p[1]):
    created = created or datetime.now()
    lines.append(f'- [{title}](/blog/{slug}.html) ({created.strftime("%A, %B %-d, %Y")})')

output_file = output_dir / 'index.html'
output_file.write_text(template.render(
    content=Markup(md.parse('\n'.join(lines)))
))

# Copy CSS files
shutil.copy('style.css', output_dir)
shutil.copy('highlight.css', output_dir)

print('build finished')
