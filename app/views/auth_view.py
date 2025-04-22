from app import db
from app.models import User
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy.exc import IntegrityError
from app.utils.auth import encode_jwt




def register_user(data):
    """Register a new user in the system.
    
    Args:
        data: Dictionary containing user registration data with keys:
            - username: Unique username
            - password: User password
            - email_id: Valid email address
            - user_role: Optional role (defaults to 'user')
    
    Returns:
        tuple: (response dictionary, HTTP status code)
            Success: {'Message': 'Registration Successful'}, 201
            Error: Error message with appropriate status code
    
    Raises:
        SQLAlchemyError: If database operation fails
    """
    try:
        username = data.get('username')
        password = data.get('password')
        email_id = data.get('email_id')
        user_role = data.get('user_role','user')

        if not username or not password or not email_id:
            return { 'Message': 'username, passowrd and email are required'},400
        
        password_hash = generate_password_hash(password)

        user = User(username=username,
                     password=password_hash,email_id=email_id,
                     user_role=user_role)
        db.session.add(user)
        db.session.commit()

        return {'Message': 'Registration Successful'},201
    except IntegrityError:
        db.session.rollback()
        return {'Message':'Username or email already exists'},400
    except Exception as e:
        return {'Message':f'Error: {str(e)}'},500
    

def login_user(data):
    """Authenticate user and generate JWT token.
    
    Args:
        data: Dictionary containing login credentials with keys:
            - username: User's username
            - password: User's password
    
    Returns:
        tuple: (response dictionary, HTTP status code)
            Success: Returns JWT token and user details, 200
            Error: Error message with appropriate status code
    """
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password,password):
        return {
            'Message': 'Invalid login'
        },401
    
    token = encode_jwt(user)
    return {
        'access_token': token,
        'user': {
            'id': user.id,
            'username': user.username,
            'role.': user.user_role
        }
    },200
    


        
