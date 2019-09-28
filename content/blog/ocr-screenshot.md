# Blessed screenshot OCR

I decided that I want to talk about [my general computer
setup](https://github.com/slint/dotfiles)... But I don't want to do this in one
big write-up. For starters, there's the the obvious benefit of stretching this
topic into multiple posts and keeping readers hooked onto what's gonna be the
next chapter in this epic saga of dotfiles. It's also much easier for me to
just pick a cool small or medium-sized part of my current setup and write a
thorough overview of what was the original need for the thing, what was my
process to find the solution, and how I implemented it and use it on my
day-to-day life.

So let's kick it off amigos!

## What in tarnation...

In this modern age of computing there's yet another way to split the masses:

- people that understand the concept of **data**
- people that just **see** stuff on the screen

The second category usually also fails to get around the magic of abstractions
and the general concept of composition:

- **Documents** are made out of **paragraphs**. **Paragraphs** are made out of
  **sentences**. **Sentences** are made out of **words**.
- **Websites** are made out of **pages**. Pages are made out of **images**,
  **text**, etc.

This is an important concept, because you cannot have **the whole** without its
individual **parts**. And here's where this is important:

![Twat email...](/images/error-mail.png)

Dear idiot. Why on earth did you decide to share this information with me in
this format? I mean it's obvious that you are on a computer. It's obvious that
you have a pointing device (otherwise you couldn't possibly navigate the damn
website), which means you could select and copy-paste the text. But you decided
not to... Why do I have to do go through a man-made CAPTCHA to help you out?

One day I turned on my computer and decided that this has to stop. I've heard
enough fearmongering about the fact that computers can now *"see"* and
*"feel"*, so I'm going to give in and actually make use of their senses.

## flameshot!

From time to time I need to take screenshots of stuff and annotate them, e.g.
when I want to put a big red arrow to point out what's a UI problem on a page.
Windows and MacOS come with some default software to do that, but on Linux you
have to do some digging... I found
[flameshot](https://github.com/lupoDharkael/flameshot) and I like it because:

1. it's pretty straightforward and powerful
2. you can call it from the CLI and it honours shell piping

So this looks something like:

```shell
flameshot gui -p ~/Pictures/screenshots/oof.png
```

## OCR for the masses

When I stumbled upon [Tesseract
OCR](https://github.com/tesseract-ocr/tesseract), I couldn't believe it... Last
time I tried to play around with OCR for automation purposes, was something
like 5 years ago and I had to use some free trial Adobe software on Windows,
where you had to run a background service thingy that every 10min processed a
folder of images and eventually spit out the results in a different folder. Or
maybe I was just 5 years younger and infinitely more naive and stupid. We'll
never truly know...

So here we are, in the year 2019 you can just:

```shell
$ sudo apt install tesseract-ocr
$ tesseract some-image-with-text.jpg stdout
Lorem ipsum dolores...
```

## The clipboard

Very often text from my terminal has to end up in other places. Grabbing my
mouse, selecting this text and copy-pasting like a peasant is not an option,
since I actively try to promote elitist CLI-only propaganda to my peers. If
they caught me in action doing such low-life maneuvers, I would lose all the
respect and external validation I'm craving for...

Thankfully, tools like `xclip`, `xsel` and `pbcopy`, make putting stuff on your
clipboard pretty easy. Even better, I'm using `zsh` with
[`oh-my-zsh`](https://github.com/robbyrussell/oh-my-zsh), which comes with
[`clipcopy`](https://github.com/robbyrussell/oh-my-zsh/blob/17f4cfca99398cb5511557b8515a17bf1bf2948a/lib/clipboard.zsh#L18),
a multi-platform shell function that allows you to do things like:

```shell
$ echo 'it be like this sometimes' | clipcopy
# These condescending words are in my clipboard now

$ clipcopy gorilla-warfare.txt
# I can now respond to insults properly via ctrl+v
```

## With their powers combined...

If you've been reading up to this point, you might be starting to see where
this is going. Prepare your eyes for this one-liner:

```shell
$ flameshot gui --raw | tesseract stdin stdout | xclip -in -selection clipboard
```

Let's break it down to a simple version with the commands split line-by-line:

```shell
# 1. Open the flasmehot GUI and to select an rectangular area from my screen
# and put the resulting image in a file
$ flameshot gui --raw > some-screenshot.png

# 2. Run Tesseract OCR on the screenshot above and put the result in a file
tesseract some-screenshot.png some-text.txt

# 3. Put the text from the file in my clipboard
xclip -in -selection clipboard

# 4. ???

# 5. Profit!
```

And here you go, yet another plague of society solved via almost a century's
worth of technology!
