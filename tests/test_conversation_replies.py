import os

import pytest
from slack_sdk.web import SlackResponse

from slapy.conversation_replies_api import ConversationRepliesAPI, ConversationRepliesParams
from tests import my_vcr


class TestConversationHistory:
    # TODO: 失敗系のテストを書く

    @pytest.fixture()
    def api(self) -> ConversationRepliesAPI:
        token = os.environ['TEST_USER_TOKEN']
        return ConversationRepliesAPI(token=token)

    @pytest.fixture()
    def TEST_CHANNEL_ID(self) -> str:
        return os.environ['TEST_CHANNEL_ID']

    @pytest.fixture()
    def TEST_THREAD_TS(self) -> str:
        return os.environ['TEST_THREAD_TS']

    @my_vcr.use_cassette('test_conversation_history/test_call_api_ok.yaml')
    def test_call_api_ok(self, api: ConversationRepliesAPI, TEST_CHANNEL_ID: str, TEST_THREAD_TS: str):
        params = ConversationRepliesParams(channel_id=TEST_CHANNEL_ID, thread_ts=TEST_THREAD_TS)
        response: SlackResponse = api.do(params)

        assert response.status_code == 200
