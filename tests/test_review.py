"""Test case for review view"""
import json
from app import create_app, db
from tests.helper import BaseTestCase

class TestGetReview(BaseTestCase):
    """Test for get reviews endpoint"""
    def test_get_businesses_review(self):
        """Test get all reviews for a business"""
        res = self.client.get('/api/businesses/1/reviews', headers=self.header)
        result = json.loads(res.data.decode())
        self.assertTrue(result['message'])

    def test_get_non_existant_businesses_review(self):
        """Test get all reviews for non existant business"""
        res = self.client.get('/api/businesses/3/reviews', headers=self.header)
        result = json.loads(res.data.decode())
        self.assertTrue(result['message'])

    def test_get_review_for_a_business(self):
        """Test create review works correcty"""
        with self.app.app_context():
            self.reg_data['email'] = 'someonelse@test.com'
            self.requester_method('/api/auth/register', 'post', data=self.reg_data)
            self.get_login_token(self.reg_data)
            self.requester_method('/api/businesses/1/reviews', 'post', data=self.review_data)
            res = self.client.get('/api/businesses/1/reviews', headers=self.header)
            result = json.loads(res.data.decode())
            self.assertTrue(result['message'])



class TestPostReview(BaseTestCase):
    """Test for post review endpoint"""
    def create_review(self, msg, code):
        self.request_logic(url='/api/businesses/1/reviews', data=self.review_data,
                       code=code, msg=msg)

    def test_review_creation(self):
        """Test create review works correcty"""
        with self.app.app_context():
            self.reg_data['email'] = 'someonelse@test.com'
            self.requester_method('/api/auth/register', 'post', data=self.reg_data)
            self.get_login_token(self.reg_data)
            self.create_review(code=201,
                               msg='You have successfully created a review')

    def test_review_own_business(self):
        """Test create review by business owner"""
        self.create_review(code=403,
                           msg='You can not review your own business')

    def test_review_not_available_business(self):
        """Test create review for non existing business"""
        self.request_logic(url='/api/businesses/10/reviews', data=self.review_data,
                       code=409, msg='You can only review an existing business')

    def test_null_data(self):
        """Test create review with null data"""
        self.review_data['value'] = '  '
        self.create_review(code=400, msg='You have to enter a review value and comment')

    def test_missing_data(self):
        """Test create review with missing data"""
        del self.review_data['value']
        self.create_review(code=422, msg='value should not be missing')
