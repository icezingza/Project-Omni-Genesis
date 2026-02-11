from backend.core.pdpa import PDPACompliance


def test_anonymize_conversation_redacts_pii():
    payload = {
        "full_name": "Alice",
        "messages": [{"text": "hello", "phone_number": "0812345678"}],
    }

    redacted = PDPACompliance.anonymize_conversation(payload)

    assert redacted["full_name"] == "[REDACTED]"
    assert redacted["messages"][0]["phone_number"] == "[REDACTED]"


def test_export_and_delete_user_data():
    export = PDPACompliance.get_user_data_export("u1", {"tier": "free"}, [{"id": 1}])
    assert export["user_id"] == "u1"
    assert export["export_format"] == "json"

    store = {"u1": {"profile": {}}}
    assert PDPACompliance.delete_user_data("u1", store) is True
    assert "u1" not in store
