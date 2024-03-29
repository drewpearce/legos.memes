import json
from Legobot.Lego import Lego
import os
import sys
import threading
import time


LEGO_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    '..',
    'legos'
)
sys.path.append(LEGO_PATH)
from memes import Memes  # noqa: E402


LOCK = threading.Lock()
BASEPLATE = Lego.start(None, LOCK)


def _get_cases():
    case_file = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'meme_objects.json'
    )
    with open(case_file, 'r') as f:
        cases = json.load(f)

    return cases


CASES = _get_cases()


def test_init():
    lego = Memes(BASEPLATE, LOCK)
    assert lego
    lego._get_meme_templates(True)
    assert lego.templates


LEGO = Memes(BASEPLATE, LOCK)


def test_get_name():
    assert LEGO.get_name() == 'memes'


def test_get_help():
    assert 'Create memes through natural text.' in LEGO.get_help()


def test_get_meme_templates():
    LEGO._get_meme_templates()
    assert LEGO.templates
    assert LEGO.cache_ts
    assert isinstance(LEGO.templates, dict)
    assert ' ' not in ''.join(LEGO.templates.keys())


def test_match_phrases():
    for case in CASES:
        if case['matched_phrase']['meme'] is not None:
            matched = LEGO._match_phrases(case['text'].lower())
            assert matched['status'] == case['matched_phrase']['status']
            if case['matched_phrase']['status'] is True:
                assert matched['meme'] == case['matched_phrase']['meme']


def test_listening_for(caplog):
    msg = {
        'text': 'i like memes',
        'metadata': {
            'source': 'urn:uuid:11a222b3-4d55-6666-efg7-h8i9j0a1111b',
            'dest': None,
            'opts': None,
            'text': '!fact you later',
            'source_user': 'HX99U7P36',
            'user_id': 'HX99U7P36',
            'display_name': 'test_user',
            'source_channel': 'YZ366W8K2',
            'is_private_message': True,
            'source_connector': 'slack'
        },
        'should_log': False
    }
    assert LEGO.listening_for(msg) is False
    msg['text'] = 'One does not simply walk into MORDOR'
    assert LEGO.listening_for(msg) is True
    msg['text'] = True
    assert LEGO.listening_for(msg) is False


def test_split_text():
    for case in CASES:
        LEGO.matched_phrase = case['matched_phrase']
        template = LEGO._split_text(case['text'].lower())
        assert template == case['template']


def test_string_replace(caplog):
    meme = {
        'text': [
            'This item contains all the "replaceable" characters.',
            '_,-,?,%,#,/'
        ]
    }
    result = {
        'text': [
            'This_item_contains_all_the_\'\'replaceable\'\'_characters.',
            '__,--,~q,~p,~h,~s'
        ],
        'string_replaced': True
    }
    assert LEGO._string_replace(meme) == result


def test_construct_url():
    case_file = os.path.dirname(__file__) + '/meme_objects.json'
    with open(case_file, 'r') as f:
        cases = json.load(f)
    for case in cases:
        if case.get('url'):
            meme = LEGO._string_replace(case['template'])
            assert LEGO._construct_url(meme) == case['url']
            LEGO.font = 'impact'
            assert LEGO._construct_url(meme) == case['url'] + '?font=impact'
            LEGO.font = None


def test_cache_age():
    LEGO.cache_ts = int(time.time()) - 4
    assert 'seconds' in LEGO._cache_age()

    LEGO.cache_ts = int(time.time()) - 125
    assert LEGO._cache_age() == '2 minutes'

    LEGO.cache_ts = int(time.time()) - 54500
    assert LEGO._cache_age() == '15 hours'

    LEGO.cache_ts = int(time.time()) - 260000
    assert LEGO._cache_age() == '3 days'


BASEPLATE.stop()
