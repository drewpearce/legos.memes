from Legobot.Lego import Lego
import requests
import logging
import json
import time

logger = logging.getLogger(__name__)


class Memes(Lego):
    def listening_for(self, message):
        if message['text'] is not None:
            try:
                triggers = ['y u no', 'yo dawg']
                text_in = message['text'].lower()
                return any(phrase in text_in for phrase in triggers)
            except Exception as e:
                logger.error('''Memes lego failed to check message text:
                            {}'''.format(e))
                return False

    def handle(self, message):
        logger.debug('Handling message...')
        opts = self._handle_opts(message)
        # Set a default return_val in case we can't handle our crap
        return_val = '¯\_(ツ)_/¯'
        matched_phrase = self._parse_args(message)
        image_id = self._get_image_id(matched_phrase)
        if image_id:
            make_image_status = self._make_image(image_id, message)
            if make_image_status:
                image = self._get_image(make_image_status)
                if image:
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

    def _parse_args(self, message):
        triggers = ['y u no', 'yo dawg']
        matched_phrases = [phrase for phrase in triggers if phrase in
                           message['text'].lower()]
        return matched_phrases[0]

    def _get_image_id(self, matched_phrase):
        url = '''https://memecaptain.com/api/v3/src_images/?q={}'''.format(
                matched_phrase)
        api_response = requests.get(url)
        if api_response.status_code == requests.codes.ok:
            api_response = json.loads(api_response.text)
            image_id = api_response[0]['id_hash']
        else:
            image_id = None
        return image_id

    def _make_image(self, image_id, message):
        url = 'https://memecaptain.com/api/v3/gend_images'
        payload = {
            "src_image_id": image_id,
            "private": False,
            "captions_attributes": [{
                "text": message['text'],
                "top_left_x_pct": 0.05,
                "top_left_y_pct": 0,
                "width_pct": 0.9,
                "height_pct": 0.25
            }]
        }
        payload = json.dumps(payload)
        # You can have memecaptain save your generated images.
        # Register with them ang get a token. In sert it below after token=.
        # Then uncomment lines 80-81 and comment out line 82.
        # auth = 'Token token='
        # headers = {"Content-Type": "application/json", "Authorization":auth}
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
            time.sleep(1)
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

    def get_name(self):
        return 'memes'

    def get_help(self):
        return 'make memes'
