from repositories.user_repository import UserRepository

class AuthService:
    @staticmethod
    def authenticate(username, password, requested_role=None):
        # Normalize username
        username_lower = username.lower().strip() if username else ''
        password = password.strip() if password else ''
        
        # All logins use: edip / edip123
        if username_lower == 'edip' and password == 'edip123':
            if requested_role == 'Student':
                user = UserRepository.get_by_username('edip_student')
                if not user:
                    user = UserRepository.create('edip_student', 'edip123', 'Student')
                return user
            elif requested_role == 'Admin':
                user = UserRepository.get_by_username('edip_admin')
                if not user:
                    user = UserRepository.create('edip_admin', 'edip123', 'Admin')
                return user
            elif requested_role == 'Instructor':
                user = UserRepository.get_by_username('edip_instructor')
                if not user:
                    user = UserRepository.create('edip_instructor', 'edip123', 'Instructor')
                return user
        
        # Also check if edip users exist and password matches
        if username_lower == 'edip':
            if requested_role == 'Student':
                user = UserRepository.get_by_username('edip_student')
                if user and UserRepository.verify_password(user, password):
                    return user
            elif requested_role == 'Admin':
                user = UserRepository.get_by_username('edip_admin')
                if user and UserRepository.verify_password(user, password):
                    return user
            elif requested_role == 'Instructor':
                user = UserRepository.get_by_username('edip_instructor')
                if user and UserRepository.verify_password(user, password):
                    return user
        
        # Normal authentication for other users
        user = UserRepository.get_by_username(username_lower)
        if user and UserRepository.verify_password(user, password):
            return user
        return None
    
    @staticmethod
    def get_user(user_id):
        return UserRepository.get_by_id(user_id)




