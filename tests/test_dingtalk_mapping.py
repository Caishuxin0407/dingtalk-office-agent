import json

from app.dingtalk_bot import get_employee_from_sender


def test_known_sender_maps_to_employee(monkeypatch):
    user_map = {
        "test_sender_001": "蔡淑欣",
    }

    monkeypatch.setenv(
        "DINGTALK_USER_MAP",
        json.dumps(user_map),
    )

    assert (
        get_employee_from_sender("test_sender_001")
        == "蔡淑欣"
    )


def test_unknown_sender_is_rejected(monkeypatch):
    monkeypatch.setenv(
        "DINGTALK_USER_MAP",
        json.dumps({}),
    )

    assert get_employee_from_sender("unknown_sender") is None


def test_invalid_mapping_configuration_is_rejected(monkeypatch):
    monkeypatch.setenv(
        "DINGTALK_USER_MAP",
        "not-valid-json",
    )

    assert get_employee_from_sender("test_sender_001") is None

