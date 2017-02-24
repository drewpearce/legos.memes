# legos.memes

[![Travis](https://travis-ci.org/drewpearce/legos.memes.svg)]()

Automatically create memes based on phrasing in this memes lego. Built using the [memecaptain API](https://github.com/mmb/meme_captain_web/tree/master/doc/api), with inspiration derived from the [Hubot memecaptain API implementation](https://www.npmjs.com/package/hubot-meme)

The Lego module system and Legobot are a FOSS project lovingly crafted by [Bren Briggs](https://github.com/bbriggs) and friends. All code borrowed from Legobot is his (C).

## Usage
This lego is invoked simply by speaking in meme phrases. Currently the following memes are supported (case insensitive.)
- `y u know...`
 - Generates a Y U No guy meme with your text on it.
- `yo dawg...`
 - Generates an Xzibit Yo Dawg meme with your message text on it.

## Installation

**Not yet published on pypi**
- Clone the repo
- cd into the directory
- `pip3 install .`

This is a Lego designed for use with [Legobot](https://github.com/bbriggs/Legobot), so you'll get Legobot along with this. To deploy it, import the package and add it to the active legos like so:

```python
# This is the legobot stuff
from Legobot import Lego
# This is your lego
from legos.memes import Memes

# Legobot stuff here
lock = threading.Lock()
baseplate = Lego.start(None, lock)
baseplate_proxy = baseplate.proxy()

# Add your lego
baseplate_proxy.add_child(Memes)
```

## Tweaking

While you can use this one as-is, you could also add a localized version to your Legobot deployment by grabbing [memes.py](legos/memes.py) and deploying is as a local module. [Example of a Legobot instance with local modules](https://github.com/voxpupuli/thevoxfox/)

## Contributing

As always, pull requests are welcome.
