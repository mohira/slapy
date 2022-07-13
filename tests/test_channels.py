import os

import pytest
from slack_sdk.web import SlackResponse

from slapy.channels import Channels
from slapy.conversation_list_api import ConversationListAPI, ConversationListParams
from tests import my_vcr


class TestChannels:
    # TODO: 失敗系のテストを書く

    class TestConversationListAPIのResponseから復元できる:
        @pytest.fixture()
        def response(self) -> SlackResponse:
            token = os.environ['TEST_USER_TOKEN']
            api = ConversationListAPI(token=token)
            params = ConversationListParams()
            return api.do(params)

        @my_vcr.use_cassette('test_channels/from_response.yaml')
        def test_from_response(self, response: SlackResponse):
            channels = Channels.from_response(response)

            assert len(channels) == 185

            assert len(channels.publics()) == 183
            assert len(channels.privates()) == 2

            assert len(channels) == len(channels.publics()) + len(channels.privates())
