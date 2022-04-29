import json
from pathlib import Path

import vcr
from dotenv import load_dotenv

load_dotenv()


def mask_response_messages():
    def before_record_response(response):
        d = json.loads(response['body']['string'])
        d['messages'] = '{{MASKED DATA}}'

        response['body']['string'] = json.dumps(d).encode()
        return response

    return before_record_response


cassettes_dir = Path(__file__).parent / 'fixtures/cassettes'

my_vcr = vcr.VCR(
    serializer='yaml',
    cassette_library_dir=str(cassettes_dir),
    record_mode='once',
    filter_headers=['authorization'],
    before_record_response=mask_response_messages(),
)
