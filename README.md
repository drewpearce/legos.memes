# legos.memes

[![Travis](https://img.shields.io/travis/drewpearce/legos.memes.svg)]() [![PyPI](https://img.shields.io/pypi/pyversions/legos.memes.svg)]() [![PyPI](https://img.shields.io/pypi/v/legos.memes.svg)]()

[![PyPI](https://img.shields.io/pypi/wheel/legos.memes.svg)]() [![PyPI](https://img.shields.io/pypi/l/legos.memes.svg)]() [![PyPI](https://img.shields.io/pypi/status/legos.memes.svg)]()

Automatically create memes based on phrasing in this memes lego. Built using the [memegen API](https://memegen.link/api/), with inspiration derived from the [Hubot memecaptain API implementation](https://www.npmjs.com/package/hubot-meme)

The Lego module system and Legobot are a FOSS project lovingly crafted by [Bren Briggs](https://github.com/bbriggs) and friends. All code borrowed from Legobot is his (C).

## Usage
### Autodetect
This lego is invoked simply by speaking in meme phrases. Currently the following memes are supported (case insensitive.)
- `y u no...`
  - Generates a Y U No guy meme with your text on it.
- `yo dawg...`
  - Generates an Xzibit Yo Dawg meme with your message text on it.
- `what if I told you...`
  - Generates a Morpheus What if I told you meme with your message text on it.
- `memexy ...all the...`
  - Generates a Hyperbole and a Half X all the Y meme with your message text on it.
- `one does not simply...`
  - Generates a Boromir One does not simply meme with your message text on it.
- `brace yourselves...`
  - Generates a Ned Stark brace yourselves meme with your message text on it.
- `why not both`
  - Generates a Why don't we have both girl meme.
- `ermahgerd...`
  - Generates a Ermahgerd! girl meme with your message text on it.
- `NO!`
  - Generates a Grumpy Cat meme.
- `i have no idea what i'm doing`
  - Generates a Computer Dog meme.
- `it's a trap`
  - Generates an Admiral Ackbar meme.
- `can't... if you don't ...`
  - Generates a Roll Safe meme with your message on it.
- `aliens guy: ...`
  - Generates an Ancient Aliens Guy memer with your message on it.

### Manual Invocation
You can also generate memes manuall through the syntax `<keyword>: <top line text>, <bottom line text>`

If you only want one line of text, simply don't include the comma.

Example: `fry: not sure if ai, or really fast coder` would generate this meme: ![Fry Meme](https://memegen.link/fry/not_sure_if_ai/or_really_fast_coder.jpg)

You can get a list of keywords in chat via `!help memes list` or you can visit [Meme Keyword List](https://memegen.link/api/templates/)

## Installation

`pip3 install legos.memes`

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
