from Legobot.Lego import Lego
import requests
import logging
import json
import time

logger = logging.getLogger(__name__)


class Memes(Lego):
    def __init__(self, baseplate, lock, *args, **kwargs):
        super().__init__(baseplate, lock)
        self.triggers = ['y u no', 'yo dawg', 'what if i told you',
                         'all the', 'one does not simply', 'brace yourselves',
                         'i don\'t always', 'not sure if', 'success kid',
                         'aliens guy', 'dat ']
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
        image_id = self._get_image_id(self.matched_phrase['meme'])
        if image_id is not None:
            meme_text = self._build_meme_text(message['text'].lower())
            make_image_status = self._make_image(image_id, meme_text)
            if make_image_status:
                image = self._get_image(make_image_status)
                if image is not None:
                    return_val = image
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

    def _get_image_id(self, matched_phrase):
        special_cases = {'y u no': 'NryNmg', 'yo dawg': 'Yqk_kg',
                         'what if i told you': 'fWle1w', 'all the': 'Dv99KQ',
                         'one does not simply': 'da2i4A', 'brace yourselves':
                         '_I74XA', 'i don\'t always': 'V8QnRQ', 'not sure if':
                         'CsNF8w', 'success kid': 'AbNPRQ', 'aliens guy':
                         'sO-Hng', 'dat ': 'CnRs9g'}
        if matched_phrase in special_cases:
            image_id = special_cases[matched_phrase]
        else:
            image_id = None
        return image_id

    def _make_image(self, image_id, message):
        url = 'https://memecaptain.com/api/v3/gend_images'
        payload = {
            "src_image_id": image_id,
            "private": False,
            "captions_attributes": [{
                "text": message,
                "top_left_x_pct": 0.05,
                "top_left_y_pct": 0,
                "width_pct": 0.9,
                "height_pct": 0.25
            }]
        }
        payload = json.dumps(payload)
        # You can have memecaptain save your generated images.
        # Register with them and get a token. Insert it below after token=.
        # Then uncomment lines 85-86 and comment out line 89.
        # auth = 'Token token='
        # headers = {"Content-Type": "application/json", "Authorization": auth}
        headers = {"Content-Type": "application/json"}
        image_response = requests.post(url, data=payload, headers=headers)
        logger.debug(payload)
        print(image_response)
        make_image_status = image_response.text
        logger.debug('Make Image response: {}'.format(make_image_status))
        return make_image_status

    def _get_image(self, make_image_status):
        status_json = json.loads(make_image_status)
        status = status_json['status_url']
        image = None
        while image is None:
            time.sleep(.5)
            get_image = requests.get(status)
            if get_image.status_code == requests.codes.ok:
                logger.debug('get_image = {}'.format(get_image.text))
                image_json = json.loads(get_image.text)
                logger.debug('image_json = {}'.format(image_json))
                if image_json['url']:
                    image = image_json['url']
                else:
                    image = None
            else:
                image = None

        return image

    def _match_phrases(self, text_in):
        matched = {}
        matched['status'] = any(phrase in text_in for phrase in self.triggers)
        for meme in self.triggers:
            if meme in text_in:
                matched['meme'] = meme
        return matched

    def _build_meme_text(self, message_text):
        messages_no_change = ['y u no', 'yo dawg', 'what if i told you',
                              'all the', 'one does not simply',
                              'brace yourselves', 'i don\'t always',
                              'not sure if', 'dat ']
        messages_trigger = ['success kid', 'aliens guy']
        if self.matched_phrase['meme'] in messages_no_change:
            return message_text
        elif self.matched_phrase['meme'] in messages_trigger:
            return message_text.replace(self.matched_phrase['meme'], '')

    def get_name(self):
        return 'memes'

    def get_help(self):
        return 'make memes'
