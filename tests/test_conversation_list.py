import os

import pytest
from slack_sdk.web import SlackResponse

from slapy.conversation_list_api import ConversationListAPI, ConversationListParams
from tests import my_vcr


class TestConversationList:
    # TODO: 失敗系のテストを書く

    @pytest.fixture()
    def api(self) -> ConversationListAPI:
        token = os.environ['TEST_USER_TOKEN']
        return ConversationListAPI(token=token)

    @my_vcr.use_cassette('test_conversation_list/test_call_api_ok.yaml')
    def test_call_api_ok(self, api: ConversationListAPI):
        params = ConversationListParams()
        response: SlackResponse = api.do(params)

        assert response.status_code == 200
