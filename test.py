from App import app
import unittest

class AppTest(unittest.TestCase):

    #check for response 200
    def test_index(self):
        tester=app.test_client(self)
        response=tester.get("/login")
        statuscode=response.status_code
        self.assertEqual(statuscode,200)

    # check if user can login correctly with correct credentials
    def test_correct_login(self) :
        tester=app.test_client(self)
        response = tester.post('/login', data=dict(username='Lukas',password='123'), follow_redirects=True)
        self.assertIn(b'Logged in successfully', response.data) 

    # check if user can'not login correctly with incorrect credentials
    def test_incorrect_login(self) :
        tester=app.test_client(self)
        response = tester.post('/login', data=dict(username='Lukas',password='124'), follow_redirects=True)
        self.assertIn(b'Incorrect username / password', response.data)  
 

    # check if user can register
    def test_user_registeration(self):
        tester=app.test_client(self)
        response = tester.post('/register', data=dict(username='Tim38', email='Tim@gmail.com',password='123'))
        self.assertIn(b'You have successfully registered', response.data)
    
    # errors during an incorrect user registration
    def test_incorrect_user_registeration(self):
        tester=app.test_client(self)
        response = tester.post('/register', data=dict(username='Thania', email='Thania',password='123'))
        self.assertIn(b'Invalid email address', response.data)
    
           
            
    
if __name__=="__main__":
       unittest.main()
 