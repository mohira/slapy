from slack_sdk.errors import SlackApiError


class InvalidAuthError(SlackApiError):
    pass


class ChannelNotFoundError(SlackApiError):
    pass


class MissingScopeError(SlackApiError):
    pass


class UndefinedClientError(SlackApiError):
    pass
