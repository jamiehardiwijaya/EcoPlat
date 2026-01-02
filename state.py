class AppState:
    current_user = None
    
    @classmethod
    def login(cls, user):
        cls.current_user = user
    
    @classmethod    
    def logout(cls):
        cls.current_user = None
        
    @classmethod
    def is_logged_in(cls):
        return cls.current_user is not None
    
    @classmethod
    def get_user_id(cls):
        return cls.current_user['id'] if cls.current_user else None
    
    @classmethod
    def get_user_name(cls):
        return cls.current_user['nama'] if cls.current_user else None
    
    @classmethod
    def get_user_email(cls):
        return cls.current_user['email'] if cls.current_user else None
        
    @classmethod
    def set_user_name(cls, new_name):
        if cls.current_user:
            cls.current_user['nama'] = new_name
            
    @classmethod
    def set_user_email(cls, new_email):
        if cls.current_user:
            cls.current_user['email'] = new_email
        
    