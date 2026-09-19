"""Adapter-agnostic event helpers for matcher integration tests."""

from itertools import count
from typing import Any

from nonebot.adapters import Event

_SEQUENCE = count()


class FakeMessageEvent(Event):
    """Minimal message event carrying a fallback `UniMessage` value."""

    message: Any
    user_id: str = "user"
    session_id: str = "session"
    to_me: bool = True

    def get_type(self) -> str:
        return "message"

    def get_event_name(self) -> str:
        return "message"

    def get_event_description(self) -> str:
        return str(self.message)

    def get_user_id(self) -> str:
        return self.user_id

    def get_session_id(self) -> str:
        return self.session_id

    def get_message(self) -> Any:
        return self.message

    def is_tome(self) -> bool:
        return self.to_me


def make_message(message: str) -> Any:
    """Build the fallback `UniMessage` value test events carry."""
    from nonebot_plugin_alconna.uniseg.fallback import FallbackMessage

    return FallbackMessage(message)


def make_event(message: str) -> FakeMessageEvent:
    """Build a test message event from plain text.

    Each event gets its own session id because alconna caches the `UniMessage` it
    parses per message id, and a fake adapter falls back to the session id.
    """
    return FakeMessageEvent(
        message=make_message(message),
        session_id=f"session-{next(_SEQUENCE)}",
    )
