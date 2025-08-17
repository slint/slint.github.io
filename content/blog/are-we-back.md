# Are we back?

It's been almost 6 years since the last time I wrote...
Of course things changed, but I'm also very much the same dude in my own special way.
I looked back at my then (M27) writings, and boy did I sound like a complete idiot.
Youthful hate towards random stuff, unaturally strong opinions (where did they come from!?), a pursuit of purity, and a very personalized sense of "simplicity".

Raw, uncapped *cringe*...
as I was saying, very much the same dude!

But why am I here again you may ask?
And why didn't I write all these years?
In some sort of "reverse ghosting" fashion, I'll pretend like nothing happened and just start writing again...

...or maybe I can be transparent about it.
My reasons for stopping are sort of common for personal tech blogs:

- **Not any "burning" ideas to write about:**: setting up your personal development environment feels fun, but it's also kind of vanilla content.
It's definitely nice to see other folks' posts on how they've customized their shell or use `tmux` in cool ways.
But the times I've radically changed my day-to-day interactions with the machines are fewer nowadays.
- **I didn't have much time:** (mostly) work, friends, family, (long-distance) relationships...
How can one just be life-ing and at the same time find time to **do** things, and **write** about it?
- **It didn't run!** A couple of years ago, I considered writing again and went ahead to build the blog as a first meaningful step.
I couldn't build the damn blog!
To be honest, with a couple more years of software engineering experience under my belt, I kind of expected that.
My homebrewed Python script with an accompanying `requirements.txt` was a classic "unreproducible summer intern project"...

And that's kind of it I guess...
It ultimately boils down to friction and lack of motivation.
The reality that in order to _do the thing_, you now have to also do some unknown "chore" beforehand.

But nonetheless, here I am again!

## _"Oh no, we here because of AI..."_

I feel like some asshole VC/founder on Twitter for saying this, but **yes, we are!**
I know I'm not the first or last to discover or talk about how ["AI changes everything"](https://lucumr.pocoo.org/2025/6/4/changes/).
But I have an undeniably good experience with using AI (well, LLMs to be precise) since the beginning of 2025.

Yes, I've had the usual wild goose chase or red herring from time to time.
I remember ChatGPT hallucinating an entire Python library and when confronted about it, go all [_"You got me..."_, Walter White style](https://youtu.be/FeAY1__jE6E?si=V1S0fLTdSJqn0E84).

But I can also see how it has removed a lot of the friction and lack of motivation I mentioned above.
It has acted as some form of "task lubricant" (_and yes, I stand by this choice of words!_) for just trying things that I would normally dimsiss as chores.
I can now throw chores to Claude Code or Gemini and sometimes even get something extra out of it.
And they really don't mind, they're designed to be these tireless hyperactive "yes"-entities.

---

I'll go through a few of the things I've achieved using AI tools in these past months.
It's a random bag of experiences that ended up forming my outlook on the effectiveness of the current tooling.

### Reviving the blog

It took Claude Code about 15-20min and about 1-2 guidance interactions to fix this blog.
It didn't care about having to go through the API changes `mistune` introduced in the latest major release.
It also didn't care though about being "smart"; getting things done is what it's built for, and that it does relentlessly.

I realized also that I, myself don't care about my blog being "smart" anymore.
It's one of many programs that just converts Markdown to HTML.
**The ideas** behind this might be somewhat "smart" and esoteric (i.e. handling Markdown headers and other elements, getting created/updated timestamps from `git`) at the time I thought of them.
But the program itself has to be simple and work reliably, exactly because it's just a means to an end: making my writting easy to publish on the internet.

### Migrating Python apps from `pipenv` to `uv`

Back in 2018 I was high on reading about how [dependency resolution is an NP-hard problem](https://pip.pypa.io/en/stable/topics/more-dependency-resolution/).
I tried to soak in all the discussion in the OG [pypa/pip#988](https://github.com/pypa/pip/issues/988) GitHub issue and marvelled at how [`@pradyunsg`](https://github.com/pradyunsg) was writing about rolling out a [new dependency resolver](https://github.com/pypa/pip/issues/6536) that would (re)solve all of our problems using *✨ m a t h s ✨*.

I also appreciated [`pip-tools`](https://github.com/jazzband/pip-tools) and [`pipenv`](https://pipenv.pypa.io/en/latest/) for trying to solve this problem in a practical manner, bringing a nice developer experience to Python dependency management.
I thought _"wow, `pipenv` even made it into [the offical Python dependency management guides](https://packaging.python.org/en/latest/tutorials/managing-dependencies/#installing-pipenv), Kenneth Reitz must be the GOAT and if we're not using this, we might as well just switch to JS"_.

That was my personal "million-hour" mistake.
`pipenv` gradually degraded into one of the slowest dependency locking experiences in the ecosystem (taking several minutes to resolve in our builds), Kenneth Reitz kind of ghosted the project (as he also did [in a much more unpleasant way with `requests`](https://vorpus.org/blog/why-im-not-collaborating-with-kenneth-reitz/)), and its unstable future became the matter of many discussions.
I can't imagine how horrible the maintainers of `pipenv` must have felt at the time, trying to keep this open-source mess up and going in such a negative atmosphere.

After having collectively wasted many hours in our projects waiting for `pipenv` to lock/install dependencies, seeing [`uv`](https://docs.astral.sh/uv/) eat everyone's lunch was a pleasant surprise, which I thought might bring an end to all of our Python packaging woes.
I tried `uv` locally for a almost a year with good results, so I started shilling it hard to my colleagues.
We slowly integrated it into our tooling and released support for it behind a flag.

And now when folks asked *"`uv` when?"*, I could respond *it's already there*.
There was one last problem: how does one migrate their project to use `uv`?

#### Take 0: *"I'll do it"* 🧑‍💻

I took it upon myself to convert my project from `pipenv` to `uv` by hand.
I knew all the `uv` features I thought were necessary, so I just went for it.

I started moving some of the package metadata fields (i.e. `title`, `license`, etc.).
Then I moved dependencies and entrypoints...
But this started feeling tedious, the format had changed and I found myself doing vim macros and whatnot to automatically fix double-quote wrapping and curly brackets.
I'm cool with that, but I can also imagine this will feel like a chore to most folks...

#### Take 1: *"Do it for me"* 🤖

Well, as I mentioned, chores are a solved problem for AI, it just chugs through!
So I moved 3-4 entries from each section and then sent off Claude Code to "do as I did".
It did so, an also tested that the file was working by running some basic `uv sync ...` and `uv pip install ...` commands.
I just left it running and eventually come back to it until it had things in a good state.

#### Take 2: *"Explain how to do it"* 🤖 → 📚

I realized that asking everyone to "just throw AI at it" was probably not a great look for the project...
But I had a clean atomic commit now showing exactly how this could be done.
I guess referencing that might be enough for someone to follow along?

Sending Git patches around might still be too much to ask though, we're not Linux kernel developers after all.
Walking someone through the diff though...
That's something we anyways do when looking at code.
And AI is actually pretty good at doing that too, it just spits out words, putting context to the words that came before them.

And thus, I asked AI to explain the commit diff and write a guide on how one could apply the same changes in their project.
It came back with a decent Markdown document, that after a few edits would be on par with the usual migration guides you see in the wild.

#### Take 3: *"Write a script to do it!"* 🤖 → 📜

After watching [Armin's video on agentic coding](https://www.youtube.com/watch?v=nfOVgz_omlU), one thing stuck out to me:
AI is not really good at actually "doing things".
And that's why we hook-up "tool calling" and "MCP servers" to allow it to escape its box and have an impact on the real world.
But even with all that, it's not a reliable executor...

You know what really has an impact on the real world, reliably every time?
It's **CODE**, brother!
Literally the act of putting a piece of soul in the machine and letting it off to do again and again the same thing, getting the right result every single time for a bunch of different scenarios.

The best tool that AI has is not "tool calling" or "MCP servers"...
**Writing code** is the best tool AI has in its disposure: one machine, plucking out of our collective ether logic threads, weaving a new soul and placing it in a bottle, creating another machine.

Similar to my "Take 1", I let Claude Code go off, but now with a task to write a script that does the set of changes I had already done to any project.
And that it did, in the well-known loop of "write, test, debug".
I tested the script in a few repositories in the wild, asked Claude Code to fix any bugs and called it a day.
I ended up opening a pull request with both the documentation and script, emphasizing parts where one probably needs to spend some manual efforts.

### Fixing my slow `zsh` startup

I recently moved from [Oh-My-Zsh](https://ohmyz.sh/) (OMZ) to [`zinit`](https://github.com/zdharma-continuum/zinit).
With OMZ, I slowly noticed my shell startup time getting longer and longer.
My years of blindly appending to my `.zshrc` every snippet for better Python/Node environment management and CLI tool autocompletions, rendered my shell numb.
I would open a new `tmux` pane, start typing frantically `cd <tab>` and then get no completions for like **3-5 seconds**.

After migrating my config to `zinit` I ended up with something much more simple.
After some `zprof` profiling, it still took **1-3 seconds** before the shell could respond to autocompletion...

These few seconds of delay might sound like nothing, but it felt like an eternity.
I like my interactions with everyday tools to feel snappy.
When I pickup a pen to write, it doesn't take 3 seconds to spill out ink!

`zinit` might be a great tool, but its sub-commands are very esoteric (and I bet it's with good intentions).
The docs for `zinit ice ...` say "*ice is zinit's options command. The option melts like ice and is used only once*"...
Sounds cool, but I don't know that this means and I just want my shell to "go brrrr!".
I tried all the tricks I could think of, but I had reached a dead-end.
Profiling wasn't helpful at all, the output was chaotic and without a clear culprit...

I've gone through multiple iterations over the years for keeping [my dotfiles](https://github.com/slint/dotfiles) tidy.
My latest attempt is using [GNU Stow](https://www.gnu.org/software/stow/manual/stow.html), the OG "symlink farm manager" (I don't know what my role in this farm is, but I'm happy to be involved!).
The cool thing is that in the end it's just a GitHub repo and all the files are in a single directory...

...which means I can unleash Claude Code upon them to just figure out what the heck is wrong!
This felt a bit risky of course, since besides reading the dotfiles, Claude might also have to run some commands to profile the startup time and see that things work.
Thus, I considered it wise to vet all the commands that Claude suggested.

And in the end it figured things out!
It changed the order of some of the commands, used `zinit wait'1 lucid ...`, and initialized some autocompletions inside a background process.
Looking at the diff, I understood the techniques and did some of my own and moved things around to further improve and tidy things up.
Without ever having to completely read the obscure `zinit` docs, my shell takes now less than 0.3sec to load!

### Making automated messsage alerts look nice

We're using [Mattermost](https://mattermost.com/) at work as the official messaging solution for internal communication, and it's fantastic.
Like many messaging platforms, it supports setting up webhooks for channels that you can then use to send arbitrary messages.
This is an excellent solution for when e.g. you have a script or monitoring service that needs to send off an alert.

What I wanted to do, is run a script every Monday morning in one of our VMs, to check some storage quota and give us a heads up in case we're running out of space.
Some colleagues had already a version of that script that produced an info-dump in plaintext to send via email.
Reading the Mattermost docs on [incoming webhooks](https://developers.mattermost.com/integrate/webhooks/incoming/) gave me some first pointers on the payload format.
I quickly put my script together, and got a decent "info dump"-style of message:

![Simple alert message (some values are edited/omitted)](/images/basic-mm-alert.png)

It wasn't the prettiest thing in the world, but squeezing 20-30% out of the docs and tweaking information density to get more polished visuals didn't feel like a good use of time.
Even if I had a free junior/intern developer I would have hesitated to throw them the task, there are more important things (like real bugs) to work on.

---

A couple of weeks passed, and the Monday message felt like a thorn on my side, my eyes purposefully avoiding to parse the raw unformatted numbers, cringing at the lack of a clear number to tell me if "we're good" or not.
I resisted the tempation to open up the script and change it (there were obviously more important things to do)...
I reconsidered though my approach on delegating the task to someone, and that "someone" ended up being Claude Code.

So far I've been treating my prompting with some care.
In the end I want to give the LLMs a fair chance at understanding an solving what I ask from them.
This time I felt that spending more than a minute on this would be overkill, so I did what every PM would:
I took a screenshot of the message, pasted it in Claude Code, added a link to the Mattermost docs, and just said "make this look nice, use whatever features/libraries you think would help".

I moved on to do something else, and after ~20min, a notification went off on Mattermost.
A new webhook message arrived showing the report, this time formatted using *every* feature that a Mattermost message could hold, emojis, ASCII-art and the whole shebang.
It was not *exactly* what I wanted, but the needle had definitely moved towards the right direction.

I retook my screenshot, annotated on it what I didn't like and explained in the prompt with more detail what I wanted different.
~15min later, we're back with the following message:

![Enhanced alert message (some values edited/omitted)](/images/enhanced-mm-alert.png)

---

None of the above experiences I wrote about sound like impressive achievements or life-changing work.
At their best, they might be described as well-supervised efforts of a junior developer.

For me and many others, documenting their existence is what makes them important.
Which leads us to my next point...

## ...the point of *"self"* in this moment

Very existential, I know.
But what's the point of even writing anymore for capturing the "human experience" in the year of our lord 2025?
Anyone can do what I did and get similar results.
Are these hacking experiences "genuine", in the same spirit of the ones I used to write about 6 years ago?
What kind of "creative process" exists in all this?

These and other questions, eventually come up when discussing with other developers about AI, its use, and how it changes our industry and everyday life.
I would have never imagined being in this situation when I started my career as a software engineer, having such fundamentally existensial discussions about our way forward.

If you haven't read [Asimov's Robot series](https://en.wikipedia.org/wiki/Robot_series), I urge you to do so, more than ever in these times.
Many of the patterns we see today like hallucinations, prompt engineering, and knowledge-worker automation, were actually already written about... **in the '50s**!

There are stories going around about field experts and sci-fi authors asked to make predictions for humanity's future when it comes to the use of technology.
Sci-fi authors made much more realistic predictions and have [a pretty good track record](https://en.wikipedia.org/wiki/List_of_existing_technologies_predicted_in_science_fiction).
I imagine scientists and field experts are obviously more "bullish" in their predictions: they have skin in the game!

This is why I am also extra-sceptical when listening to executives of AI (or AI-adopter) companies making big statements regarding big percentages of the workforce becoming obsolete in just a couple of years.

---

Given all the noise, I crave for a "control sample" to exist in this grand experiment.

### _**I want my written thoughts, to trully be my very own.**_

So what I write in this blog is 100% typed by my human hands and always will be.

It's not a matter of virgin creation or anything like this.
Novel ideas are rare, we're anyways all just mashing together bits and pieces of information we read on a tweet or listened on a podcast, and sometimes remember to link back to that trail.

I was considering to pass a draft of this blogpost to some big-brain model for copy-editing and maybe a first review to see if it all "flows right".
I did so, and as I started reading its review, felt all the mistakes and narrative issues wash over something I had spent writing over a decent part of 4 weekends.
Unlike a piece of code being reviewed, this piece of writing actually reflects a piece of myself.

If I am to phase it through the "primordial token soup" of an LLM, I might as well paint it blue and throw it in the ocean.
My out-of-place references to `zprof`, Python dependency tooling, and Asimov, all to be stripped away for the sake of clarity and to satisfy short attention spans.

And well, here we are now.
I've been left by myself to cook.
The result might be ugly, but at least it came from my own garden.
