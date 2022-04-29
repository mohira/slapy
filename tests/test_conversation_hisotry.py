import os

import pytest
from slack_sdk.errors import SlackApiError

from slapy.client_errors import InvalidAuthError, MissingScopeError
from slapy.conversation_history_api import ConversationHistoryAPI, ConversationHistoryParams
from tests import my_vcr


class TestConversationHistory:

    @pytest.fixture()
    def api(self) -> ConversationHistoryAPI:
        return ConversationHistoryAPI(token=os.environ['TEST_USER_TOKEN'])

    @pytest.fixture()
    def TEST_CHANNEL_ID(self) -> str:
        return os.environ['TEST_CHANNEL_ID']

    class TestClientError:
        @my_vcr.use_cassette()
        def test_invalid_token(self, TEST_CHANNEL_ID: str):
            api = ConversationHistoryAPI(token='INVALID_TOKEN')

            with pytest.raises(InvalidAuthError):
                api.do(ConversationHistoryParams(TEST_CHANNEL_ID))

        @my_vcr.use_cassette()
        def test_channel_not_found(self, api: ConversationHistoryAPI):
            params = ConversationHistoryParams(channel_id='INVALID_CHANNEL_ID')
            with pytest.raises(SlackApiError):
                api.do(params)

        @my_vcr.use_cassette()
        @pytest.mark.skip(reason='missing scopeを再現する方法が謎なのでSKIP')
        def test_missing_scope(self, api: ConversationHistoryAPI, TEST_CHANNEL_ID: str):
            with pytest.raises(MissingScopeError):
                api.do(ConversationHistoryParams(TEST_CHANNEL_ID))
