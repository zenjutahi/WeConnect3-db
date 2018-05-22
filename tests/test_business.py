"""Test case for business view"""
import json
from app import db
from tests.helper import BaseTestCase


class TestPostBusiness(BaseTestCase):
    """Test for post business endpoint"""
    def register_business(self, msg, code):
        self.request_logic(url='/api/businesses', data=self.business_data,
                       code=code, msg=msg)

    def test_business_creation(self):
        """Test create business works correcty"""
        result = json.loads(self.biz_res.data.decode())
        self.assertEqual(result['message'], "New business has been created")
        self.assertEqual(self.biz_res.status_code, 201)

    def test_empty_name(self):
        """Test create business with space as name"""
        self.business_data['name'] = '   '
        self.register_business(code=403, msg='You need a business name and' +
                                                        ' location to Register')

    def test_null_name(self):
        """Test create business with space as name"""
        del self.business_data['name']
        self.register_business(code=422, msg='name should not be missing')

    def test_already_registered_name(self):
        """Test create business with already registered name"""
        self.register_business(code=409, msg='This Business is' +
                                                        ' already registered')


    def test_valid_json_request(self):
        """Test edit business request is json format"""
        del self.header['Content-Type']
        self.register_business(msg='Bad Request. Request should be JSON format',
                                                                    code=400)

class TestPutBusiness(BaseTestCase):
    """Test for editing business endpoint"""
    def edit_business(self, msg, code):
        self.business_data['name'] = 'Mandela'
        self.request_logic(url='/api/businesses/1', data=self.business_data,
                       method='put', code=code, msg=msg)

    def test_business_can_be_edited(self):
        """Test edit an existing business works as expected"""
        self.edit_business(code=201, msg='Business edited successfully')

    def test_existant_name_for_edited_business(self):
        """Test edit a business with an existant name"""
        self.business_data['name'] = 'a2Z Ict'
        self.request_logic(url='/api/businesses/1', code=409,
                                    data=self.business_data, method='put',
                                    msg='This Business is name is already used')

    def test_missing_edit_data(self):
        """Test edit business with missing input"""
        del self.business_data['category']
        self.edit_business(code=422, msg='category should not be missing')

    def test_non_existing_business(self):
        """Test edit business that is not available"""
        self.request_logic(url='/api/businesses/2', data=self.business_data,
                         method='put',code=404, msg='Bussniess does not exist')
    def test_user_not_logged_in(self):
        """Test delete by unregistered user"""
        with self.app.app_context():
            del self.header['Authorization']
            res = self.requester_method(url='/api/businesses/1', method='delete',
                                    data=self.business_data)
            result = json.loads(res.data.decode())
            self.assertEqual(result['msg'], 'Missing Authorization Header')

    def test_empty_name(self):
        """Test create business with space as name"""
        self.business_data['description'] = '   '
        self.edit_business(code=403, msg='Business name and Location'+
                                            ' have to be entred')

    def test_valid_json_request(self):
        """Test edit business request is json format"""
        del self.header['Content-Type']
        self.edit_business(msg='Bad Request. Request should be JSON format',
                                                                    code=400)


class TestDeleteBusiness(BaseTestCase):
    """Test for delete business endpoint"""
    def delete_business(self, msg, code):
        self.request_logic(url='/api/businesses/1', method='delete',
                       data=self.password, code=code, msg=msg)

    def test_business_can_be_deleted(self):
        """Test delete an existing business"""
        self.delete_business(code=202, msg='Business successfully deleted')

    def test_delete_non_existing_business(self):
        """Test edit business that is not available"""
        self.request_logic(url='/api/businesses/2', data=self.business_data,
                    method='delete', code=404, msg='Bussniess does not exist')

    def test_delete_another_user_business(self):
        """Test delete a business that user did not create"""
        with self.app.app_context():
            self.reg_data['email'] = 'anotheruser@test.com'
            self.requester_method('/api/auth/register', 'post',
                                            data=self.reg_data)
            self.get_login_token(self.reg_data)
            self.delete_business(code=403,
                                 msg='You can only change your own business')

    def test_user_not_loged_in(self):
        """Test delete by and None logged in user"""
        with self.app.app_context():
            del self.header['Authorization']
            res = self.requester_method(url='/api/businesses/1',
                                    method='delete', data=self.business_data)
            result = json.loads(res.data.decode())
            self.assertEqual(result['msg'], 'Missing Authorization Header')


class TestGetBusiness(BaseTestCase):
    """Test for get business endpoint"""
    def get_business(self,  url):
        res = self.client.get(path=url, headers=self.header)
        return json.loads(res.data.decode())

    def test_all_businesses(self):
        """Test get all registered businesses"""
        result = self.get_business('/api/businesses')
        # print(result)
        self.assertEqual(result['message'], 'These are the businesses')

    def test_a_single_businesses(self):
        """Test get all registered businesses"""
        result = self.get_business('/api/businesses/1')
        # print(result)
        self.assertEqual(result['message'], 'Here is the searched business')

    def test_empty_businesses(self):
        """Test get all with no registered businesses"""
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            self.requester_method('/api/auth/register', 'post',
                                             data=self.reg_data)
            self.get_login_token(self.reg_data)
            result = self.get_business('/api/businesses')
            self.assertEqual(result['message'], 'No businesses available')

class TestFilterBusiness(BaseTestCase):
    """Test for filter business endpoint"""
    def filter_business(self,  url):
        res = self.client.get(path=url, headers=self.header)
        return json.loads(res.data.decode())

    def test_filter_businesses_by_category(self):
        """Test filter registered businesses by category"""
        result = self.filter_business('/api/businesses/filter?' +
                                                        'category=Technology')
        self.assertEqual(result['message'],
                         'Businesses successfully filtered')

    def test_filter_businesses_not_found(self):
        """Test filter businesses not found"""
        result = self.filter_business('/api/businesses/filter?' +
                                                        'category=farming')
        self.assertEqual(result['message'],
                         'No businesses found')

    def test_filter_business_with_wrong_pagination(self):
        """Test filter business with wrong pagination"""
        result = self.filter_business('/api/businesses/filter?'+
                                                'category=Technology&page=t')
        self.assertEqual(result['message'],
                         'Invalid pagination limit or page')


class TestSearchBusiness(BaseTestCase):
    """Test for search business endpoint"""
    def search_business(self,  url):
        res = self.client.get(path=url, headers=self.header)
        return json.loads(res.data.decode())

    def test_search_businesses(self):
        """Test search registered businesses"""
        result = self.search_business('/api/businesses/search?q=a2z')
        self.assertEqual(result['message'],
                         "Here's the search result")
    def test_search_businesses_retuening_none(self):
        """Test search non-registered businesses"""
        result = self.search_business('/api/businesses/search?q=jeff')
        self.assertEqual(result['message'],
                      "No businesses found")

    def test_search_business_with_wrong_pagination(self):
        """Test search business with wrong pagination"""
        result = self.search_business('/api/businesses/search?q=ict&page=t')
        self.assertEqual(result['message'],
                         'Invalid pagination limit or page')
