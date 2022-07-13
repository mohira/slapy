from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from slack_sdk.web import SlackResponse


@dataclass(frozen=True)
class Member:
    id: str
    name: str
    real_name: str


@dataclass(frozen=True)
class Members:
    values: List[Member] = field(default_factory=list)

    def add(self, m: Member) -> Members:
        return Members(self.values + [m])

    def __len__(self) -> int:
        return len(self.values)

    def __getitem__(self, index: int) -> Member:
        return self.values[index]

    @classmethod
    def from_response(cls, response: SlackResponse) -> Members:
        members = Members()

        for m in response['members']:
            is_bot = (m['id'] == 'USLACKBOT') or (m['is_bot'])
            if is_bot:
                continue

            member = Member(id=m['id'], name=m['name'], real_name=m['profile']['real_name'])
            members = members.add(member)

        return members
