# import json
# import pytest
# from app import app
# from models import db, User

# @pytest.fixture
# def client():
#     app.config['TESTING'] = True
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
#     with app.test_client() as client:
#         with app.app_context():
#             db.create_all()
#             # Create a test user
#             test_user = User(username='testuser')
#             test_user.set_password('password123')
#             db.session.add(test_user)
#             db.session.commit()
#             yield client
#             db.session.remove()
#             db.drop_all()

# def test_register(client):
#     """Test user registration"""
#     response = client.post('/register', json={
#         'username': 'newuser',
#         'password': 'securepassword',
#         'email': 'newuser@example.com'
#     })
#     data = json.loads(response.data)
    
#     assert response.status_code == 201
#     assert data['message'] == 'User registered successfully'
    
#     # Verify the user exists in database
#     with app.app_context():
#         user = User.query.filter_by(username='newuser').first()
#         assert user is not None
#         assert user.email == 'newuser@example.com'
#         assert user.check_password('securepassword')

# def test_login_success(client):
#     """Test successful login"""
#     response = client.post('/login', json={
#         'username': 'testuser',
#         'password': 'password123'
#     })
#     data = json.loads(response.data)
    
#     assert response.status_code == 200
#     assert 'access_token' in data
#     assert data['username'] == 'testuser'

# def test_login_invalid_credentials(client):
#     """Test login with invalid credentials"""
#     response = client.post('/login', json={
#         'username': 'testuser',
#         'password': 'wrongpassword'
#     })
#     data = json.loads(response.data)
    
#     assert response.status_code == 401
#     assert 'Invalid credentials' in data['message']

# def test_login_missing_fields(client):
#     """Test login with missing fields"""
#     response = client.post('/login', json={
#         'username': 'testuser'
#     })
#     data = json.loads(response.data)
    
#     assert response.status_code == 400
#     assert 'Missing required fields' in data['message']

# def test_protected_route_with_token(client):
#     """Test accessing protected route with valid token"""
#     # First login to get token
#     login_response = client.post('/login', json={
#         'username': 'testuser',
#         'password': 'password123'
#     })
#     login_data = json.loads(login_response.data)
#     token = login_data['access_token']
    
#     # Access protected route
#     response = client.get('/api/profile',
#                           headers={'Authorization': f'Bearer {token}'})
#     data = json.loads(response.data)
    
#     assert response.status_code == 200
#     assert data['username'] == 'testuser'

# def test_protected_route_without_token(client):
#     """Test accessing protected route without token"""
#     response = client.get('/api/profile')
#     data = json.loads(response.data)
    
#     assert response.status_code == 401
#     assert 'Token is missing' in data['message']