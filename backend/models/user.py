import bcrypt

def create_user(db, username, email, password):
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = {
        "username": username,
        "email": email,
        "password": hashed_pw
    }
    db.users.insert_one(user)
    return str(user["_id"])

def find_user_by_email(db, email):
    return db.users.find_one({"email": email})

def check_password(user, password):
    return bcrypt.checkpw(password.encode('utf-8'), user['password'])
