from dataclasses import dataclass
from dataclasses import field
from typing import Optional
from urllib.error import URLError

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.web import SlackResponse

from slapy.client_errors import InvalidAuthError, MissingScopeError, UndefinedClientError


@dataclass(frozen=True)
class ConversationListParams:
    cursor: Optional[str] = None
    exclude_archived: Optional[bool] = None
    limit: Optional[int] = None
    team_id: Optional[str] = None
    types: Optional[str] = None


@dataclass(frozen=True)
class ConversationListAPI:
    """https://api.slack.com/methods/conversations.list"""
    token: str
    sdk: WebClient = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, 'sdk', WebClient(self.token))

    def do(self, p: ConversationListParams) -> SlackResponse:
        try:
            return self.sdk.conversations_list(cursor=p.cursor,
                                               exclude_archived=p.exclude_archived,
                                               limit=p.limit,
                                               team_id=p.team_id,
                                               types=p.types)
        except SlackApiError as e:
            error = e.response['error']

            if error == 'invalid_auth':
                raise InvalidAuthError(f'無効なトークンです: {self.token}', e)
            if error == 'missing_scope':
                raise MissingScopeError('スコープがおかしいよ', e)

            raise UndefinedClientError('未定義のエラーなので登録してくれ', e)
        except URLError as e:
            # ネットが死んでたらアウツ
            raise e
