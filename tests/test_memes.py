import json
from Legobot.Lego import Lego
import os
import sys
import threading


LEGO_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '..',
        'legos'
    )
)
sys.path.append(LEGO_PATH)
from memes import Memes  # noqa: E402

LOCK = threading.Lock()
BASEPLATE = Lego.start(None, LOCK)
LEGO = Memes(BASEPLATE, LOCK)
EX_MSG = {
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


def test_get_name():
    assert LEGO.get_name() == 'memes'


def test_get_help():
    assert LEGO.get_help() == ('Create memes through natural text. See '
                               'https://github.com/drewpearce/legos.memes/blob'
                               '/master/README.md for reference.')


def test_handle_opts(caplog):
    msg = EX_MSG
    opts = LEGO._handle_opts(msg)
    assert isinstance(opts, dict)
    assert opts.get('target') == msg['metadata']['source_channel']

    LEGO._handle_opts({'metadata': {}})
    assert 'Could not identify message source in message' in caplog.text


def test_match_phrases():
    # TODO: Add more test cases.
    cases = [
        {
            'case': 'Legobot, y u no have tests?!',
            'meme': ' y u no ',
            'status': True
        },
        {
            'case': 'This text does not trigger.',
            'status': False
        }
    ]

    for case in cases:
        matched = LEGO._match_phrases(case['case'])
        assert matched['status'] == case['status']
        if case['status'] is True:
            assert matched['meme'] == case['meme']


def test_listening_for(caplog):
    msg = EX_MSG
    assert LEGO.listening_for(msg) is False
    msg['text'] = 'One does not simply walk into MORDOR'
    assert LEGO.listening_for(msg) is True


def test_split_text():
    case_file = os.path.dirname(__file__) + '/meme_objects.json'
    with open(case_file, 'r') as f:
        cases = json.load(f)
    for case in cases:
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


BASEPLATE.stop()
