# Initial commit: how I built my blog

Hey y'all, I decided to start a blog! I've been thinking of doing so for a
while now and as the saying goes, *"there's no better time than the present"*.
This is not meant to be a steady *one-post-per-week* kind of thing (god
forbid...), but more of an occasional brain dump of things I come across at
work/personal time and I'd like to write about. Most of these "things" will
probably be programming-related, but I might sneak in a couple of other topics,
like music, TV-series/movies, and other normal-people stuff if I feel fancy.

I feel that while writing code is a big part of a developer's life, **any
writing** in general should also be something one practices to be able to
document and communicate things in a better/faster/easier way. Also, to hell
with it, if you feel like doing something, just do it!

In order to not just keep two puny paragraphs of an explanation to why I want
to write about stuff and post it online, I also thought it would be nice to
give an actual example of something I would write about. I built this blog from
scratch and this is what I'll talk about.

## Why build it from scratch?

1. People use things like [Lektor](https://www.getlektor.com/),
   [Hugo](https://gohugo.io/) and [Jekyll](https://jekyllrb.com/) to generate
   static websites. These tools are perfectly fine for setting up something
   quickly which looks good and holds content, and at the end of the day I'm
   just one guy that wants to write some Markdown and put it on the internet.
   Sounds like a good fit right?

   **Wrong!** What exactly is so complicated about creating `3 +
   (number-of-blog-posts)` pages that look decent, to the point that I need
   [bloody ReactJS](https://www.gatsbyjs.org/) to do it?

   I mean, I'm all behind "reusable code" and "don't reinvent the wheel", but
   for something as simple as converting a bunch of Markdown files (written by
   one person at any moment) to HTML, a handful of lines of code to glue
   together a couple core libraries shouldn't be that much work.

2. I want to end up with something that feels unique and personal. Even if I
   decided to customize one of the above tools/frameworks, it would still feel
   like a cookiecutter-website, in the same fashion that when I see a Bootstrap
   or Wordpress website I know how it was made.

3. At the time I'm writing this people seem to really like writing blog posts
   on a site called [Medium](https://medium.com/) and its related site
   [Hackernoon](https://hackernoon.com). I used to think that content that ends
   up there has a certain quality. Nowadays, **I absolutely hate this
   website...** It seems to tick every box on the 2019 list of "Things that
   will mildly annoy you while you're trying to read some actual content, to
   the point of disgust". It has paywall-like pop-ups. It has
   privacy/cookie/ToS/whatever bars at the bottom. It has ads. It has
   permanently floating top and bottom bars with the website logo, the menu and
   some mumbo-jumbo about subscribing to a newsletter.

   The combination of all these, plus a general lack of good typography, make
   this website one of the worst experiences I've ever had for the simple act
   of reading 15 minutes of text. If I ever happen to have someone read my
   depressing blobs of text, I would like them to get offended by the actual
   content and not the lack of a good delivery method.

4. **It's a fun and easy thing to do!** How long ago was it that you just had
   to write simple code that does simple stuff? After a while on the job you
   lose this luxury... It was a very pleasant change to start thinking in a
   minimalist but pragmatist way of building something that will reliably do
   one thing well and won't get in your way while you try to edit your actual
   content.

## So how does it work?

There's a folder called `content`. If you put `<name>.md` files in there, they
will get converted into `<name>.html` pages served at the root of the website
(e.g.
[`content/about.md`](https://github.com/slint/slint.github.io/blob/source/content/about.md)
becomes [/about.html](/about.html)). `.md` files in the `content/blog` folder
are *special* though, and will also be part of a generated sorted-by-date
"catalog" that lives in [index.html](/).

All this is done via the Python script called
[`build.py`](https://github.com/slint/slint.github.io/blob/source/build.py).
Running this, will generate/copy all the `.{html,css}` files in a `_build`
folder:

```python
blog_posts = []

# pathlib.Path is pure bliss to use when dealing with paths and files
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
for slug, title, created, _ in sorted(blog_posts, key=lambda p: p[1], reverse=True):
    created_str = (created or dt.now()).strftime("%A, %B %-d, %Y")
    lines.append(f'- [{title}](/blog/{slug}.html) ({created_str})')

output_file = output_dir / 'index.html'
output_file.write_text(template.render(
    content=Markup(md.parse('\n'.join(lines)))
))

# Copy CSS files
shutil.copy('style.css', output_dir)
shutil.copy('highlight.css', output_dir)
```

Some notable "fancy" stuff that happens:

- Title extraction from the Markdown files (using `mistune`'s parser):

```python
def extract_title(markdown):
    # mistune parses Markdown into tokens. the first lvl-1 header is the title
    return next((
        token['text'] for token in mistune.BlockLexer().parse(markdown)
        if token['type'] == 'heading' and token['level'] == 1
    ), None)
```

- Created/updated datetime extraction of each blog post (from the git history
  of each file):

```python
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
```

- Code highlighting using [`Pygments`](http://pygments.org):

```python
    def block_code(self, code, lang):
        if not lang:
            return f'\n<pre><code>{mistune.escape(code)}</code></pre>\n'
        lexer = pygments.lexers.get_lexer_by_name(lang, stripall=True)
        formatter = pygments.formatters.html.HtmlFormatter()
        return pygments.highlight(code, lexer, formatter)
```

- External links get opened in a new tab via generating `<a>` tags with the
  `target="_blank"` attribute:

```python
    def link(self, link, title, text):
        link = mistune.escape_link(link)
        target = ''
        if urlparse(link).netloc:
            target = 'target="_blank"'
        if not title:
            return f'<a {target} href="{link}">{text}</a>'
        title = mistune.escape(title, quote=True)
        return f'<a {target} href="{link}" title="{title}">{text}</a>'
```

## Developer/User experience

If I want to create a new blog post I just create a new `.md` file inside the
`content/blog` folder, I come up with a nice title and just start spewing out
enough non-sense to fill-up 10-20min of someone's reading time.

I like the WYSIWYG experience, where making even a small change to any kind of
file relevant to how things should render, triggers and immediate rebuild of
the result and shows it to you. Tools like [LiveReload](http://livereload.com/)
have made this kind of things pretty seamless, and as always there's a [Python
package](https://github.com/lepture/python-livereload) which brings this magic
to our fingertips. I thus have a `server.py` script which runs a LiveReload
server, monitoring `.css` and `.md` files:

```python
#!/usr/bin/env python
import subprocess
import sys

from livereload import Server

# run initial build
subprocess.run('./build.py')

server = Server()
server.watch('base.jinja2', './build.py')
server.watch('content/*.md', './build.py')
server.watch('content/blog/*.md', './build.py')
server.watch('*.css', './build.py')

open_in_browser = '-o' in sys.argv
server.serve(root='_build/', open_url=open_in_browser)
```

## Aesthetics

I'm not a CSS guru and I have to admit that I have to properly catch-up up at
some point with `display: flex`. I'm also definitely not a designer. But before
starting I had in mind some good examples of blogs/pages that I enjoy reading,
not only because of the content, but because of the simplicity of their design
and the personal/trademark impression it leaves. Some of these sources of
inspiration are:

- [Armin Ronacher aka `mitsuhiko`'s blog](http://lucumr.pocoo.org/)
- [Salvatore Sanfilippo aka `antirez`'s blog](http://antirez.com/)
- [`brandur`'s blog](https://brandur.org/articles)
- ["Web Design in 4 Minutes"](https://jgthms.com/web-design-in-4-minutes/), by
  Jeremy Thomas, creator of the Bulma CSS framework

By hacking around I ended up with [~30 lines of
CSS](https://github.com/slint/slint.github.io/blob/source/style.css) that make
the darn thing pleasant to look at.

```css
/* Google fonts are a nice way to add some "personality" */
@import url('https://fonts.googleapis.com/css?family=Quicksand&display=swap');
@import url('https://fonts.googleapis.com/css?family=Source+Code+Pro&display=swap');

body {
  margin: 0 auto;
  max-width: 50em; /* Keep a wide-enough center column for the content */
  font-family: "Quicksand", "Helvetica", "Arial", sans-serif;
  -moz-font-smoothing: grayscale;
  -webkit-font-smoothing: antialiased;
  text-align: justify;
  /* Giving things room to breathe is pretty important */
  line-height: 1.5;
  padding: 2em 1em;
  color: #444;
}

a { color: #1a5579; }
h1, h2, strong { color: #222; }
h1 { margin: 0 auto; }
h2 { padding-top: 0.5em; }

code, pre {
  background: #f5f7f9;
  border-bottom: 1px solid #d8dee9;
  font-family: 'Source Code Pro', monospace;
  font-size: 0.8em;
}
code { padding: 2px 4px; vertical-align: text-bottom; }
pre { padding: 1em; overflow: auto; border-left: 2px solid #C04144; }

header h1 { font-size: 3em; }
header h1 a { text-decoration: none; }
```

## Conclusions

It took roughly a day to develop the whole thing and about another day to write
this blog post. Normally I would spread the time it took to write the blogpost
over a week or two, but since I was on vacation I managed to put in the effort
to make something complete and also quickly address any usability issues.

I've been actually editing this post over 3-4 days, since I might rethink some
parts during the day and then feel the urge to go back to refine them. I guess
this would naturally happen over a week's time, so instead of being eager to
push changes, next time I'll try to hold on and delay putting up the final blog
post until a week's time has gone by.

At the time I have a couple of topics in mind to write about, but as I said
before, no strict schedule in terms of when I'll start working on that.

I also have a couple of small features I'd like to add to the blog like
image/files support, having draft posts (i.e. not publicly visible yet), an
RSS/Atom feed, and that's pretty much all I want to have here. I don't want to
poison this with a comments/reactions section, share buttons or any kind of
"social web" stuff.

Overall, I'm pretty happy with how this turned out! I would recommend you to
partake into this kind of experience yourselves if you can, I currently have
this warm feeling similar to when you repair or build something on your own in
your home/garden/workspace.

Last thing I guess, is addressing the oldest problem in the book, i.e. picking
a good name for the blog...
