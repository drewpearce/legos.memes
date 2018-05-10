from Legobot.Lego import Lego
import logging
import re

logger = logging.getLogger(__name__)


class Memes(Lego):
    def __init__(self, baseplate, lock, *args, **kwargs):
        super().__init__(baseplate, lock)
        self.triggers = ['memexy ', ' y u no ', 'what if i told you ',
                         'yo dawg ', 'one does not simply ',
                         'brace yourselves ', 'why not both', 'ermahgerd',
                         'no!', 'i have no idea what i\'m doing',
                         'it\'s a trap', ' if you don\'t ']
        self.matched_phrase = ''

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
        return_val = '¯\_(ツ)_/¯'
        meme = self._split_text(message['text'].lower())

        if meme is not None and meme['template'] is not None:
            meme = self._string_replace(meme)
            if meme['string_replaced'] is True and len(meme['text']) == 2:
                return_val = self._construct_url(meme)
            self.reply(message, return_val, opts)

    def _handle_opts(self, message):
        try:
            target = message['metadata']['source_channel']
            opts = {'target': target}
        except IndexError:
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

        if self.matched_phrase['meme'] == 'memexy ':
            meme['template'] = 'xy'
            message = message.replace('memexy ', '')
            meme['text'] = message.split(' all the ')
            meme['text'][1] = 'all the ' + meme['text'][1]
        elif self.matched_phrase['meme'] == ' y u no ':
            meme['template'] = 'yuno'
            meme['text'] = message.split(' y u no ')
            meme['text'][1] = 'y u no ' + meme['text'][1]
        elif self.matched_phrase['meme'] == 'what if i told you ':
            meme['template'] = 'morpheus'
            meme['text'] = ['what if i told you']
            meme['text'].append(message.split('what if i told you ')[1])
        elif self.matched_phrase['meme'] == 'yo dawg ':
            meme['template'] = 'yodawg'
            meme['text'] = re.split(' so (i|we) put ', message)
            meme['text'][2] = ('so ' + meme['text'][1] +
                               ' put ' + meme['text'][2])
            meme['text'].pop(1)
        elif self.matched_phrase['meme'] == 'one does not simply ':
            meme['template'] = 'mordor'
            meme['text'] = ['one does not simply']
            meme['text'].append(message.split('one does not simply ')[1])
        elif self.matched_phrase['meme'] == 'brace yourselves ':
            meme['template'] = 'winter'
            meme['text'] = ['brace yourselves']
            meme['text'].append(message.split('brace yourselves ')[1])
        elif self.matched_phrase['meme'] == 'why not both':
            meme['template'] = 'both'
            meme['text'] = [' ', 'why not both?']
        elif self.matched_phrase['meme'] == 'ermahgerd':
            meme['template'] = 'ermg'
            meme['text'] = ['ermahgerd!', re.split('ermahgerd.* ', message)[1]]
        elif self.matched_phrase['meme'] == 'no!':
            meme['template'] = 'grumpycat'
            meme['text'] = [' ', 'NO!']
        elif self.matched_phrase['meme'] == 'i have no idea what i\'m doing':
            meme['template'] = 'noidea'
            meme['text'] = ['i have no idea', 'what i\'m doing']
        elif self.matched_phrase['meme'] == 'it\'s a trap':
            meme['template'] = 'ackbar'
            meme['text'] = [' ', 'it\'s a trap!']
        elif self.matched_phrase['meme'] == ' if you don\'t ':
            if re.search("^can't.*if you don't.*", message):
                meme['template'] = 'rollsafe'
                meme['text'] = message.split(' if you don\'t ')
                meme['text'][1] = 'if you don\'t ' + meme['text'][1]
            else:
                meme['template'] = None
        else:
            meme['template'] = None

        return meme

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

    def get_help(self):
        return ('Create memes through natural text. See https://github.com/'
                'drewpearce/legos.memes/blob/master/README.md for reference.')
