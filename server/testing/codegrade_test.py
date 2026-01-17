
import pytest
from app import app, db
from models import Newsletter

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_newsletters.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_home_get(client):
    """Test GET / endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the Newsletter RESTful API" in response.data

def test_newsletters_get(client):
    """Test GET /newsletters endpoint"""
    response = client.get('/newsletters')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_newsletters_post(client):
    """Test POST /newsletters endpoint"""
    response = client.post('/newsletters', data={
        'title': 'Test Newsletter',
        'body': 'This is a test newsletter body.'
    })
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data['title'] == 'Test Newsletter'
    assert json_data['body'] == 'This is a test newsletter body.'

def test_newsletters_get_single(client):
    """Test GET /newsletters/<id> endpoint"""
