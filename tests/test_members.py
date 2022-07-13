from __future__ import annotations

import os

import pytest
from slack_sdk.web import SlackResponse

from slapy.members import Members
from slapy.users_list_api import UserListParams, UsersListAPI
from tests import my_vcr


class TestMembers:
    # TODO: 失敗系のテストを書く

    class TestUserListAPIのResponseから復元できる:
        @pytest.fixture()
        def response(self) -> SlackResponse:
            token = os.environ['TEST_USER_TOKEN']
            api = UsersListAPI(token=token)
            params = UserListParams()
            return api.do(params)

        @my_vcr.use_cassette('test_members/from_response.yaml')
        def test_from_response(self, response: SlackResponse):
            members = Members.from_response(response)

            assert len(members) == 1
