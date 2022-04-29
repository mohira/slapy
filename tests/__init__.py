import vcr
from dotenv import load_dotenv

my_vcr = vcr.VCR(
    serializer='yaml',
    cassette_library_dir='fixtures/cassettes',
    record_mode='once',
    filter_headers=['authorization']
)

load_dotenv()
