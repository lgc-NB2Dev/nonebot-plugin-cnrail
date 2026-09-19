"""Canned RailGo API payloads and an ``httpx`` transport that serves them."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any
from typing_extensions import Self

import httpx

if TYPE_CHECKING:
    import pytest

GET_TRAIN_MAIN = "getTrainMain"
GET_COACH_PIC = "getCoachPic"
TRAIN_PRESELECT = "train/preselect"


def timetable_item(**overrides: Any) -> dict[str, Any]:
    """Build one camelCase timetable entry as the RailGo API returns it."""
    return {
        "arrive": "13:28",
        "day": 0,
        "depart": "13:30",
        "runTime": 268,
        "station": "上海虹桥",
        "stationTelecode": "AOH",
        "stopTime": 2,
        "trainCode": "G1",
        "distance": 1318,
        **overrides,
    }


def train_main_payload(
    *,
    timetable: list[dict[str, Any]] | None = None,
    **overrides: Any,
) -> dict[str, Any]:
    """Build the camelCase ``data`` payload of a ``getTrainMain`` response."""
    return {
        "bureau": "京",
        "bureauShortName": "北京局",
        "car": "CR400AF-2001",
        "carOwner": "北京局",
        "numberFull": ["G1"],
        "numberKind": "高速",
        "rundays": ["20260919"],
        "runner": "北京局",
        "spend": 268,
        "timetable": [timetable_item()] if timetable is None else timetable,
        **overrides,
    }


def coach_pic_payload(
    *,
    car_code: str = "CR400AF-2001",
    **overrides: Any,
) -> dict[str, Any]:
    """Build the camelCase ``data`` payload of a ``getCoachPic`` response."""
    return {
        "carCode": car_code,
        "carType": "二等座",
        "trainStyle": "复兴号",
        **overrides,
    }


def v2_envelope(data: Any, *, success: bool = True, msg: str = "") -> dict[str, Any]:
    """Wrap a ``data`` payload in the RailGo v2 response envelope."""
    return {"data": data, "msg": msg, "success": success}


def search_payload(**overrides: Any) -> dict[str, Any]:
    """Build a camelCase train-search payload as the RailGo API returns it."""
    return {
        "trainNumber": "G1",
        "beginStationName": "上海虹桥",
        "departureTime": "08:00",
        "endStationName": "北京南",
        "arrivalTime": "12:28",
        "durationMinutes": 268,
        "trainType": "高速",
        **overrides,
    }


def via_station(**overrides: Any) -> dict[str, Any]:
    """Build a camelCase via-station payload as the RailGo API returns it."""
    return {
        "stationName": "上海虹桥",
        "trainNumber": "G1",
        "stopMinutes": 2,
        "dayIndex": 0,
        **overrides,
    }


def detail_data(*stations: dict[str, Any]) -> Any:
    """Build a ``TrainDetailData`` around the given via-station payloads."""
    from nonebot_plugin_cnrail.models import TrainDetailData

    payload: dict[str, Any] = {
        "trainNumber": "G1",
        "trainType": "高速",
        "companyName": "上海局",
        "viaStations": list(stations),
        "routing": {"trainModel": "CR400AF"},
    }
    return TrainDetailData(**payload)


@dataclass
class _Route:
    status: int
    json: Any
    text: str | None


class FakeRailGo:
    """Serve canned RailGo responses for every ``data_source`` request."""

    def __init__(self) -> None:
        self._routes: dict[str, _Route] = {}
        self.requests: list[httpx.Request] = []

    def route(
        self,
        path: str,
        *,
        status: int = 200,
        json: Any = None,
        text: str | None = None,
    ) -> Self:
        """Serve the given response for requests whose path ends with ``path``."""
        if json is not None and text is not None:
            msg = "pass either `json` or `text`, not both"
            raise ValueError(msg)
        self._routes[path] = _Route(status, json, text)
        return self

    def install(self, monkeypatch: "pytest.MonkeyPatch") -> Self:
        """Route every ``data_source`` request through this fake transport."""
        from nonebot_plugin_cnrail import data_source

        def make_client(base_url: str) -> httpx.AsyncClient:
            return httpx.AsyncClient(
                base_url=base_url,
                follow_redirects=True,
                transport=httpx.MockTransport(self._handle),
            )

        monkeypatch.setattr(data_source, "_make_client", make_client)
        return self

    def queries(self, path: str) -> list[dict[str, str]]:
        """Return the query parameters of every recorded request matching ``path``."""
        return [
            dict(request.url.params)
            for request in self.requests
            if request.url.path.endswith(path)
        ]

    def _handle(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        for path, route in self._routes.items():
            if request.url.path.endswith(path):
                if route.json is not None:
                    return httpx.Response(route.status, json=route.json)
                if route.text is not None:
                    return httpx.Response(route.status, text=route.text)
                return httpx.Response(route.status)
        msg = f"unexpected request to {request.url}"
        raise AssertionError(msg)


class QueuedRailGo(FakeRailGo):
    """A ``FakeRailGo`` that answers successive ``getTrainMain`` calls differently."""

    def __init__(self, main_responses: list[tuple[int, Any]]) -> None:
        """Queue one ``(status, envelope)`` pair per ``getTrainMain`` call."""
        super().__init__()
        self._main_responses = list(main_responses)

    def _handle(self, request: httpx.Request) -> httpx.Response:
        """Serve the next queued main response, delegating every other path."""
        if request.url.path.endswith(GET_TRAIN_MAIN) and self._main_responses:
            self.requests.append(request)
            status, payload = self._main_responses.pop(0)
            return httpx.Response(status, json=payload)
        return super()._handle(request)
