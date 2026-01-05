from repositories.user_repository import UserRepository

class AuthService:
    @staticmethod
    def authenticate(username, password):
        user = UserRepository.get_by_username(username)
        if user and UserRepository.verify_password(user, password):
            return user
        return None
    
    @staticmethod
    def get_user(user_id):
        return UserRepository.get_by_id(user_id)




