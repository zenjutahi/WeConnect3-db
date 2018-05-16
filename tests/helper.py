"""
Base Test case with setup and methods that other
test classes inherit
"""
import unittest
import json
import datetime
from flask_jwt_extended import create_access_token
from app import create_app, db
from app.models import Business, User


class BaseTestCase(unittest.TestCase):
    """Base Test Case"""
    def setUp(self):
        """Set up test variables"""
        self.app = create_app(config_name="testing")
        with self.app.app_context():
            self.client = self.app.test_client()
            self.expires = datetime.timedelta(minutes=2)
            self.token = create_access_token(identity='wrong@mail.com',expires_delta=self.expires)
            db.drop_all()
            db.create_all()
        self.header = {'Content-Type': 'application/json'}
        self.reg_data = {'email': 'jeff@try.com', 'username': 'Zenjutahi',
                         'first_name': 'mutahi', 'password': 'Test1234'}
        self.passwords = {'old_password': 'Test1234',
                          'new_password': 'busstest123'}
        self.reg_res = self.requester_method('/api/auth/register', 'post',
                                         data=self.reg_data)
        self.get_login_token(self.reg_data)
        self.business_data = {'name': 'a2Z Ict','description':'we do this and that',
                              'category': 'Technology',  'location': 'Mombasa'}
        self.biz_res = self.requester_method('/api/businesses', 'post',
                                         data=self.business_data)
        self.password = {'password': 'busstest123'}

        self.review_data = {'value': '4.5',
                            'comments': 'I loved your services'}




    def requester_method(self, url, method, data):
        """Make a request to the given url with the given method"""
        data = json.dumps(data)
        if method == 'put':
            return self.client.put(path=url,
                                   headers=self.header, data=data)
        elif method == 'delete':
            return self.client.delete(path=url,
                                      headers=self.header, data=data)
        return self.client.post(path=url, headers=self.header, data=data)

    def request_logic(self, url, method='post', jsons=True, **kwargs):
        """Make the test to a given url"""
        data = kwargs['data']
        message = kwargs['msg']
        code = kwargs['code']

        res = self.requester_method(url, method, data)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], message)
        self.assertEqual(res.status_code, code)

    def get_login_token(self, data):
        """Get the access token and add it to the header"""
        login_res = self.requester_method('/api/auth/login', 'post', data=data)
        result = json.loads(login_res.data.decode())
        self.header['Authorization'] = 'Bearer ' + result['access_token']
        return result

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
