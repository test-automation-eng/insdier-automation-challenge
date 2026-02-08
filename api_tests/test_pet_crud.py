import time
import random
import allure
import requests

BASE_URL = "https://petstore.swagger.io/v2"
TIMEOUT = 10


def random_pet_id():
    # safer than pure random: time + random
    return int(time.time() * 1000) + random.randint(1, 999)


def create_pet(pet_id: int, name: str, status: str = "available"):
    payload = {
        "id": pet_id,
        "name": name,
        "photoUrls": ["https://example.com/dog.png"],
        "status": status
    }
    return requests.post(f"{BASE_URL}/pet", json=payload, timeout=TIMEOUT)

@allure.title("Get pet - positive")
def test_get_pet_positive():
    pet_id = random_pet_id()
    create_pet(pet_id, "FetchMe")

    r = requests.get(f"{BASE_URL}/pet/{pet_id}", timeout=TIMEOUT)
    with allure.step("Verify created pet can be fetched"):
        assert r.status_code == 200, r.text
        assert r.json()["id"] == pet_id    

@allure.title("Create pet - positive")
def test_create_pet_positive():
    pet_id = random_pet_id()

    r = create_pet(pet_id, "AllureDog")
    with allure.step("Verify 200 and response matches"):
        assert r.status_code == 200, r.text
        data = r.json()
        assert data["id"] == pet_id
        assert data["name"] == "AllureDog"        

@allure.title("Upadte pet - positive")    
def test_update_pet_positive():
    pet_id = random_pet_id()
    create_pet(pet_id, "OldName")

    payload = {
        "id": pet_id,
        "name": "NewName",
        "photoUrls": ["https://example.com/dog.png"],
        "status": "available"
    }
    r = requests.put(f"{BASE_URL}/pet", json=payload, timeout=TIMEOUT)
    with allure.step("Verify update response"):
        assert r.status_code == 200, r.text
        data = r.json()
        assert data["id"] == pet_id
        assert data["name"] == "NewName"   

@allure.title("Delete pet - positive")
def test_delete_pet_positive():
    pet_id = random_pet_id()
    create_pet(pet_id, "ToDelete")

    r = requests.delete(f"{BASE_URL}/pet/{pet_id}", timeout=TIMEOUT)
    with allure.step("Verify delete response"):
        assert r.status_code == 200, r.text

    r2 = requests.get(f"{BASE_URL}/pet/{pet_id}", timeout=TIMEOUT)
    with allure.step("Verify pet is deleted"):
        assert r2.status_code == 404, r2.text
           