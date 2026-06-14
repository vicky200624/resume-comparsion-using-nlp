from mangodb import users_collection

def signup(username, password, role):
    if users_collection.find_one({"username": username}):
        return {"message": "User exists"}

    users_collection.insert_one({
        "username": username,
        "password": password,
        "role": role
    })

    return {"message": "Signup successful"}

def login(username, password):
    user = users_collection.find_one({
        "username": username,
        "password": password
    })

    if user:
        return {"message": "Login success", "role": user["role"]}

    return {"message": "Invalid credentials"}
