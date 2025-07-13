# My personal blog

## Usage

Make sure you have [`uv` installed](https://docs.astral.sh/uv/getting-started/installation/).

```bash
# to build:
./build.py

# to run a magical LiveReload server and open the browser:
./server.py -o

# to deploy:
./deploy.sh

# To generate code highlighting CSS:
uvx --from pygments pygmentize -S colorful -f html -a .highlight > highlight.css
```
