from datetime import date
from fastapi import status


test_contact={
    "first_name" : "First",
    "last_name" :"Last",
    "email" : "user@mail.com",
    "phone_number" : "12345689",
    "birthday": date(2010, 1, 1).isoformat(),
    "additional_info" : "additional text",
    }



def test_create_contact(client, get_token):
    response = client.post(
        "/api/contacts",
        json=test_contact,
        headers={"Authorization": f"Bearer {get_token}"},
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["first_name"] == test_contact["first_name"]
    assert "id" in data
    

def test_get_contact(client, get_token):
    response = client.get(
        "/api/contacts/1", headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["first_name"] == test_contact["first_name"]
    assert "id" in data

def test_get_contact_not_found(client, get_token):
    response = client.get(
        "/api/contacts/2", headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Contact not found"

def test_get_contacts(client, get_token):
    response = client.get("/api/contacts", headers={"Authorization": f"Bearer {get_token}"})
    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["first_name"] == test_contact["first_name"]
    assert "id" in data[0]
    assert len(data) > 0





def test_update_contact(client, get_token):
    update_test_contact = test_contact.copy()
    update_test_contact["first_name"] = "new_test_contact"
    response = client.put(
        "/api/contacts/1",
        json=update_test_contact,
        headers={"Authorization": f"Bearer {get_token}"},
    )
    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    assert data["first_name"] == update_test_contact["first_name"]
    assert "id" in data
    assert data["id"] == 1

def test_update_contact_not_found(client, get_token):
    update_test_contact = test_contact.copy()
    update_test_contact["first_name"] = "new_test_contact"
    response = client.put(
        "/api/contacts/2",
        json=update_test_contact,
        headers={"Authorization": f"Bearer {get_token}"},
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Contact not found"

def test_delete_contact(client, get_token):
    response = client.delete(
        "/api/contacts/1", headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 204, response.text
    data = response.text
    assert data == ""

def test_repeat_delete_contact(client, get_token):
    response = client.delete(
        "/api/contacts/1", headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Contact not found"

