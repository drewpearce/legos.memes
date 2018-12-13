import json
from Legobot.Lego import Lego
import logging
import re
import requests

logger = logging.getLogger(__name__)


class Memes(Lego):
    def __init__(self, baseplate, lock, *args, **kwargs):
        super().__init__(baseplate, lock)
        self.triggers = ['memexy ', ' y u no ', 'what if i told you ',
                         'yo dawg', 'one does not simply ',
                         'brace yourselves ', 'why not both', 'ermahgerd',
                         'no!', 'i have no idea what i\'m doing',
                         'it\'s a trap', ' if you don\'t ', 'aliens guy:']
        self.matched_phrase = ''
        self.templates = self._get_meme_templates()
        self.keywords = [keyword + ':' for keyword in [*self.templates]]
        self.triggers += self.keywords

    def listening_for(self, message):
        if message['text'] is not None:
            try:
                text_in = message['text'].lower()
                self.matched_phrase = self._match_phrases(text_in)
                return self.matched_phrase['status']
            except Exception as e:
                logger.error('''Memes lego failed to check message text:
                            {}'''.format(e))
                return False

    def handle(self, message):
        logger.debug('Handling message...')
        opts = self._handle_opts(message)
        # Set a default return_val in case we can't handle our crap
        return_val = r'¯\_(ツ)_/¯'
        meme = self._split_text(message['text'].lower())

        if meme is not None and meme['template'] is not None:
            meme = self._string_replace(meme)
            if meme['string_replaced'] is True and len(meme['text']) == 2:
                return_val = self._construct_url(meme)
            self.reply(message, return_val, opts)

    def _get_meme_templates(self):
        get_templates = requests.get('https://memegen.link/api/templates/')
        if get_templates.status_code == requests.codes.ok:
            templates = json.loads(get_templates.text)
            templates = {v.split('/')[-1]: k for k, v in templates.items()}
            return templates
        else:
            logger.error(('Error retrieving '
                          'templates.\n{}: {}').format(
                              get_templates.status_code,
                              get_templates.text))
            return {}

    def _handle_opts(self, message):
        try:
            target = message['metadata']['source_channel']
            opts = {'target': target}
        except LookupError:
            opts = None
            logger.error('''Could not identify message source in message:
                        {}'''.format(str(message)))
        return opts

    def _match_phrases(self, text_in):
        matched = {}
        matched['status'] = any(phrase in text_in for phrase in self.triggers)
        for meme in self.triggers:
            if meme in text_in:
                matched['meme'] = meme
        return matched

    def _split_text(self, message):
        meme = {}

        center_matches = {
            'memexy ': {
                'template': 'xy',
                'match_text': 'all the ',
                'strip_trigger': True
            },
            ' y u no ': {
                'template': 'yuno'
            }
        }

        front_matches = {
            'what if i told you ': {
                'template': 'morpheus'
            },
            'one does not simply ': {
                'template': 'mordor'
            },
            'brace yourselves ': {
                'template': 'winter'
            },
            'aliens guy:': {
                'template': 'aag',
                'strip_trigger': True
            }
        }

        single_phrases = {
            'why not both': {
                'template': 'both',
                'text': [' ', 'why not both?']
            },
            'i have no idea what i\'m doing': {
                'template': 'noidea',
                'text': ['i have no idea', 'what i\'m doing']
            },
            'it\'s a trap': {
                'template': 'ackbar',
                'text': [' ', 'it\'s a trap!']
            }
        }

        if self.matched_phrase['meme'] in center_matches.keys():
            trigger = self.matched_phrase['meme']
            meme['template'] = center_matches[trigger].get('template')
            meme['text'] = self._split_text_center_match(
                trigger,
                message,
                match_text=center_matches[trigger].get('match_text'),
                strip_trigger=center_matches[trigger].get('strip_trigger'))
        elif self.matched_phrase['meme'] in front_matches.keys():
            trigger = self.matched_phrase['meme']
            meme['template'] = front_matches[trigger].get('template')
            meme['text'] = self._split_text_front_match(
                trigger,
                message,
                strip_trigger=front_matches[trigger].get('strip_trigger'))
        elif self.matched_phrase['meme'] in single_phrases.keys():
            trigger = self.matched_phrase['meme']
            meme['template'] = single_phrases[trigger].get('template')
            meme['text'] = single_phrases[trigger].get('text')
        elif self.matched_phrase['meme'] == 'yo dawg':
            meme['template'] = 'yodawg'
            meme['text'] = re.split(' so (i|we) put ', message)
            meme['text'][2] = ('so ' + meme['text'][1] +
                               ' put ' + meme['text'][2])
            meme['text'].pop(1)
        elif self.matched_phrase['meme'] == 'ermahgerd':
            meme['template'] = 'ermg'
            meme['text'] = ['ermahgerd!', re.split('ermahgerd.* ', message)[1]]
        elif self.matched_phrase['meme'] == 'no!':
            if re.search('^no!.*', message):
                meme['template'] = 'grumpycat'
                meme['text'] = [' ', 'NO!']
            else:
                meme['template'] = None
        elif self.matched_phrase['meme'] == ' if you don\'t ':
            if re.search("^can't.*if you don't.*", message):
                meme['template'] = 'rollsafe'
                meme['text'] = message.split(' if you don\'t ')
                meme['text'][1] = 'if you don\'t ' + meme['text'][1]
            else:
                meme['template'] = None
        elif (self.matched_phrase['meme'] in self.keywords
                and message.startswith(self.matched_phrase['meme'])):
            meme['template'] = self.matched_phrase['meme'].replace(':', '')
            message = message.replace(self.matched_phrase['meme'], '')
            meme['text'] = message.split(',')
            if len(meme['text']) < 2:
                meme['text'].append(meme['text'][0])
                meme['text'][0] = ' '
            index = 0
            for line in meme['text']:
                if line != ' ':
                    meme['text'][index] = line.strip()
                index += 1
        else:
            meme['template'] = None

        if meme.get('text'):
            for i, text in enumerate(meme['text']):
                if text == '':
                    meme['text'][i] = ' '

                if meme['text'][i] != ' ':
                    meme['text'][i] = meme['text'][i].strip()

        return meme

    def _split_text_front_match(self, trigger, text, strip_trigger=False):
        if strip_trigger:
            response = [' ']
        else:
            response = [trigger]
        response.append(text.split(trigger)[1])
        return response

    def _split_text_center_match(self, trigger, text, match_text=None,
                                 strip_trigger=False):
        if not match_text:
            match_text = trigger

        if strip_trigger:
            text = text.replace(trigger, '')

        response = text.split(match_text)
        response[1] = match_text + response[1]
        return response

    def _string_replace(self, meme):
        replacements = {
            '_': '__',
            '-': '--',
            ' ': '_',
            '?': '~q',
            '%': '~p',
            '#': '~h',
            '/': '~s',
            '"': "''",
        }

        for index, text in enumerate(meme['text']):
            substrs = sorted(replacements, key=len, reverse=True)
            regexp = re.compile('|'.join(map(re.escape, substrs)))
            meme['text'][index] = \
                regexp.sub(lambda match: replacements[match.group(0)], text)

        meme['string_replaced'] = True
        logger.debug(meme)
        return meme

    def _construct_url(self, meme):
        base_url = 'https://memegen.link/'
        return (base_url + meme['template'] +
                '/' + meme['text'][0] +
                '/' + meme['text'][1] + '.jpg')

    def get_name(self):
        return 'memes'

    def get_help(self, **kwargs):
        subcommands = {
                'keywords': 'Keyword usage:'
                            '`<keyword>: <top line>, <bottom line>`'
                            'Try `!help memes list` for a list of keywords',
                'list': ', '.join(sorted([*self.templates]))
                }

        if ('sub' in kwargs):
            return subcommands[kwargs['sub']]
        else:
            return ('Create memes through natural text. '
                    'See https://github.com/'
                    'drewpearce/legos.memes/blob/master/README.md '
                    'for reference.\n'
                    'In addition to natural language, legos.memes '
                    'can create memes by keywords. '
                    'Use `!help memes keywords` for help using this feature.')
