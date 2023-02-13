from typing import List
from app.entries import entry_schema
import pytest


"""
Retrieve entries test suite
"""


def test_get_all_entries(authorized_user, test_entry, test_user):
    res = authorized_user.get("/entries/")

    def validate(entry):
        return entry_schema.EntryOut(**entry)

    entry_map = map(validate, res.json())
    entry_list = list(entry_map)
    # assert len(res.json()) == len(test_entry["owner_id": test_user['id']])
    assert res.status_code == 200


def test_get_unauthorized_entry(authorized_user, test_entry):
    res = authorized_user.get(f"/entries/{test_entry[2].id}")
    assert res.status_code == 401
    assert (
        res.json().get("detail")
        == f"Unauthorized access to get entry with id {test_entry[2].id}"
    )


def test_unauthorized_user_to_get_entry(client):
    res = client.get("/entries/")
    assert res.status_code == 401


def test_unauthorized_user_to_get_entry_by_id(client, test_entry):
    res = client.get(f"/entries/{test_entry[1].id}")
    assert res.status_code == 401


def test_get_entry_by_id_that_doesnt_exist(authorized_user):
    res = authorized_user.get(f"/entries/30")
    assert res.status_code == 404
    assert res.json().get("detail") == f"Entry with id {30} not found"


def test_get_entries_by_id(authorized_user, test_entry):
    res = authorized_user.get(f"/entries/{test_entry[0].id}")
    entry = entry_schema.EntryOut(**res.json())
    assert res.status_code == 200
    assert entry.id == test_entry[0].id
    assert entry.title == test_entry[0].title
    assert entry.content == test_entry[0].content


"""
create entry test suite
"""


@pytest.mark.parametrize(
    "title, content",
    [("Dove on clout", "Let's go!"), ("Moving tom", "I don't know easy")],
)
def test_create_entry(authorized_user, test_user, title, content):
    entry_data = {"title": title, "content": content}
    res = authorized_user.post("/entries/", json=entry_data)
    created_entry = entry_schema.EntryOut(**res.json())
    assert created_entry.title == title
    assert created_entry.content == content
    assert created_entry.owner_id == test_user["id"]
    assert res.status_code == 201


@pytest.mark.parametrize(
    "title, content",
    [
        ("Unauthorized user", "cannot create entry"),
        ("Unauthorized people", "Won't be allowed to create entry"),
    ],
)
def test_unauthorized_client_to_create_entry(client, title, content):
    entry_data = {"title": title, "content": content}
    res = client.post("/entries/", json=entry_data)
    assert res.status_code == 401


"""
delete entry test suite
"""


def test_unauthorized_user_to_delete_entry(client, test_user, test_entry):
    res = client.delete(f"/entries/{test_entry[0].id}")
    assert res.status_code == 401


def test_delete_entry_by_id_that_doesnt_exist(authorized_user):
    res = authorized_user.delete(f"/entries/90")
    assert res.status_code == 404
    assert res.json().get("detail") == f"Entry with id {90} not found"


def test_delete_entry_success(authorized_user, test_entry):
    res = authorized_user.delete(f"/entries/{test_entry[0].id}")
    assert res.status_code == 204


def test_unable_to_delete_unauthorized_entry(authorized_user, test_entry):
    res = authorized_user.delete(f"/entries/{test_entry[2].id}")
    assert res.status_code == 401
    assert (
        res.json().get("detail")
        == f"Unauthorized access to delete entry with id {test_entry[2].id}"
    )


"""
Update entry test suite
"""


def test_update_entry_success(authorized_user, test_entry):
    updated_data = {
        "title": "New title update",
        "content": "New content update",
    }
    res = authorized_user.put(
        f"/entries/{test_entry[0].id}", json=updated_data
    )
    updated_entry = entry_schema.EntryOut(**res.json())
    assert updated_entry.title == "New title update"
    assert updated_entry.content == "New content update"
    assert res.status_code == 200


def test_unable_to_update_unauthorized_entry(authorized_user, test_entry):
    updated_data = {
        "title": "New title update",
        "content": "New content update",
    }
    res = authorized_user.put(
        f"/entries/{test_entry[2].id}", json=updated_data
    )
    assert res.status_code == 401
    assert (
        res.json().get("detail")
        == f"Unauthorized access to update entry with id {test_entry[2].id}"
    )


def test_update_entry_by_id_that_does_not_exist(authorized_user):
    updated_data = {
        "title": "New title update",
        "content": "New content update",
    }
    res = authorized_user.put(f"/entries/40", json=updated_data)
    assert res.status_code == 404
    assert res.json().get("detail") == f"Entry with id {40} not found"


def test_unauthorized_user_to_update_entry(client, test_entry):
    updated_data = {
        "title": "New title update",
        "content": "New content update",
    }
    res = client.put(f"/entries/{test_entry[0].id}", json=updated_data)
    assert res.status_code == 401
