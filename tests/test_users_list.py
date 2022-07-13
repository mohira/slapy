import os

import pytest
from slack_sdk.web import SlackResponse

from slapy.users_list_api import UserListParams, UsersListAPI
from tests import my_vcr


class TestUsersList:
    # TODO: 失敗系のテストを書く

    @pytest.fixture()
    def api(self) -> UsersListAPI:
        token = os.environ['TEST_USER_TOKEN']
        return UsersListAPI(token=token)

    @my_vcr.use_cassette('test_users_list/test_call_api_ok.yaml')
    def test_call_api_ok(self, api: UsersListAPI):
        params = UserListParams()
        response: SlackResponse = api.do(params)

        assert response.status_code == 200
