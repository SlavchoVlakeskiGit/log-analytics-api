from app.core.security import create_access_token, hash_password, verify_password

fake_user = {
    "username": "admin",
    "hashed_password": hash_password("admin123"),
}


class AuthService:
    def authenticate(self, username: str, password: str) -> dict | None:
        if username != fake_user["username"]:
            return None

        if not verify_password(password, fake_user["hashed_password"]):
            return None

        return {"sub": username}

    def create_token(self, user_data: dict) -> str:
        return create_access_token(user_data)