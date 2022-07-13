from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from slack_sdk.web import SlackResponse


@dataclass(frozen=True)
class Channel:
    id: str
    name: str
    is_archived: bool
    is_private: bool


@dataclass(frozen=True)
class Channels:
    values: List[Channel] = field(default_factory=list)

    def add(self, ch: Channel) -> Channels:
        return Channels(self.values + [ch])

    def __len__(self) -> int:
        return len(self.values)

    def __getitem__(self, index: int) -> Channel:
        return self.values[index]

    def privates(self) -> Channels:
        return Channels([ch for ch in self if ch.is_private])

    def publics(self):
        return Channels([ch for ch in self if not ch.is_private])

    @classmethod
    def from_response(cls, response: SlackResponse) -> Channels:
        channels = Channels()

        for ch in response['channels']:
            ch_id = ch['id']
            name = ch['name']
            is_private = ch['is_private']
            is_archived = ch['is_archived']

            channels = channels.add(Channel(id=ch_id, name=name, is_private=is_private, is_archived=is_archived))

        return channels
