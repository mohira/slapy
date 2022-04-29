from dataclasses import dataclass
from dataclasses import field
from typing import Optional
from urllib.error import URLError

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.web import SlackResponse

from slapy.client_errors import ChannelNotFoundError, InvalidAuthError, MissingScopeError, UndefinedClientError


@dataclass(frozen=True)
class ConversationHistoryParams:
    channel_id: str
    cursor: Optional[str] = None,
    inclusive: Optional[bool] = None,
    latest: Optional[str] = None,
    limit: Optional[int] = None,
    oldest: Optional[str] = None,


@dataclass(frozen=True)
class ConversationHistoryAPI:
    """https://api.slack.com/methods/conversations.history"""
    token: str
    sdk: WebClient = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, 'sdk', WebClient(self.token))

    def do(self, p: ConversationHistoryParams) -> SlackResponse:
        try:
            return self.sdk.conversations_history(channel=p.channel_id,
                                                  cursor=p.cursor,
                                                  inclusive=p.inclusive,
                                                  latest=p.latest,
                                                  limit=p.limit,
                                                  oldest=p.oldest)
        except SlackApiError as e:
            error = e.response['error']

            if error == 'invalid_auth':
                raise InvalidAuthError(f'無効なトークンです: {self.token}', e)
            if error == 'channel_not_found':
                raise ChannelNotFoundError(f'チャンネルが見当たりませんよ: {p.channel_id=}', e)
            if error == 'missing_scope':
                raise MissingScopeError('スコープがおかしいよ', e)

            raise UndefinedClientError('未定義のエラーなので登録してくれ', e)
        except URLError as e:
            # ネットが死んでたらアウツ
            raise e
