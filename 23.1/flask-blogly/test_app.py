from unittest import TestCase
from app import app 
from models import db, User


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class FlaskTests(TestCase):
    
    def setUp(self):
        # db.db_init('postgresql:///blogly_db')
        user = User(first_name="Rick", last_name="Sanchez")
        db.session.add(user)
        db.session.commit()
        
        
    def tearDown(self):
        """Cancels commit transaction"""
        db.session.rollback()
        
    # def test_redirect(self):
    #     with app.test_client() as client:
    #         resp = client.get("/users")
    #         html = resp.get_data(as_text=True)
    #         self.assetEqual(resp.status_code, 302)
    #         self.assertIn()
        
    def test_list_users(self):
        with app.test_client() as client:
            """can make request to flask via client"""
            resp = client.get("/users")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("/users", html)
            
            
    def test_show_user(self):
        with app.test_client() as client:
            resp = client.post("/users/{self.user_id}")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 404)
            self.assertNotEqual("<h1>Jerry Xiao</h1>", html)
  
            
    
# https://www.superherodb.com/pictures2/portraits/10/050/11217.jpg?v
