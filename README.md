# My personal blog

## Usage

```bash
# create a virtualenv and install deps
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# to build:
./build.py

# to run a magical LiveReload server and open the browser:
./server.py -o

# to deploy:
./deploy.sh

# To generate code highlighting CSS:
pygmentize -S colorful -f html -a .highlight > highlight.css
```
