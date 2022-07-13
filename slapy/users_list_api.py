from dataclasses import dataclass
from dataclasses import field
from typing import Optional
from urllib.error import URLError

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.web import SlackResponse

from slapy.client_errors import InvalidAuthError, MissingScopeError, UndefinedClientError


@dataclass(frozen=True)
class UserListParams:
    cursor: Optional[str] = None
    include_locale: Optional[bool] = None
    limit: Optional[int] = None
    team_id: Optional[str] = None


@dataclass(frozen=True)
class UsersListAPI:
    """https://api.slack.com/methods/users.list"""
    token: str
    sdk: WebClient = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, 'sdk', WebClient(self.token))

    def do(self, p: UserListParams) -> SlackResponse:
        try:
            return self.sdk.users_list(cursor=p.cursor,
                                       include_locale=p.include_locale,
                                       limit=p.limit,
                                       team_id=p.team_id)
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
