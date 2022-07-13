from __future__ import annotations

import os
from pathlib import Path

import pytest

from slapy.members import Members
from slapy.to_csv import to_csv
from slapy.users_list_api import UserListParams, UsersListAPI
from tests import my_vcr


class TestToCSV:
    @pytest.fixture()
    def members(self) -> Members:
        token = os.environ['TEST_USER_TOKEN']
        api = UsersListAPI(token=token)
        params = UserListParams()

        response = api.do(params)
        return Members.from_response(response)

    @my_vcr.use_cassette('test_to_csv/members_to_csv_from_response.yaml')
    def test_members_to_csv_from_response(self, members: Members, tmp_path: Path):
        p = tmp_path / 'tmp.csv'
        to_csv(p, members)

        assert p.read_text() == 'id,name,real_name\nU62A12649,mohira,mohira\n'
