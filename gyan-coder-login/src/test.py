import hashlib
import json
def load_users():
    try:
        with open("users.json", "r") as file:
            print(json.load(file))
            return json.load(file)
    except FileNotFoundError:
        return {}
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
def verify_user(username, password):
    users = load_users()
    if username in users and users[username]["password"] == hash_password(password):
        print( users[username]["password"])
        print( users[username][password])
        print(hash_password(password))
        return True
    return False
verify_user("naveen","a1b8821b956eb35d3c256b155e330a34316a78720acb4110fbd72725ade6a673")