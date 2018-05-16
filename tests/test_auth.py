import json
from tests.helper import BaseTestCase

class TestRegisterUser(BaseTestCase):
    """Test for Register User endpoint"""
    def register(self, msg, code):
        self.request_logic('/api/auth/register', data=self.reg_data, code=code,
                      msg=msg)

    def test_registration(self):
        """Test user registration works correcty"""
        result = json.loads(self.reg_res.data.decode())
        self.assertEqual(result['message'], "New user Succesfully created")
        self.assertEqual(self.reg_res.status_code, 201)

    def test_already_registered_user(self):
        """Test that a user cannot be registered twice"""
        self.register(msg="This email is registered, login instead", code=404)

    def test_invalid_password_pattern(self):
        """Test register with short password length"""
        self.reg_data['password'] = 'les'
        self.register(code=400,
                      msg='You need email, username and password to register')

    def test_register_invalid_email(self):
        """Test user registration with an invalid email address"""
        self.reg_data['email'] = 'wrong'
        self.register(msg="Invalid Email. Enter valid email to register", code=400)

    def test_register_missing_password(self):
        """Test user registration with missing password"""
        del self.reg_data['password']
        self.register(msg='password should not be missing', code=422)

    def test_valid_json_request(self):
        """Test register request is json format"""
        del self.header['Content-Type']
        self.register(msg='Bad Request. Request should be JSON format', code=405)


class TestLoginUser(BaseTestCase):
    """Test for Login User endpoint"""
    def login(self, msg, code):
        self.request_logic('/api/auth/login', data=self.reg_data, code=code, msg=msg)

    def test_user_login(self):
        """Test registered user can login"""
        self.login(code=200, msg='Successfully Loged In')

    def test_unregistered_user_login(self):
        """Test unregistered user cannot login"""
        self.reg_data['email'] = 'notreg@test.com'
        self.login(code=401, msg='Invalid Email: Enter right credentions to login')

    def test_incorrect_password_login(self):
        """Test incorrect password cannot login"""
        self.reg_data['password'] = 'wrongpas'
        self.login(code=401, msg='Invalid password: Enter right password to login')

    def test_null_password_login(self):
        """Test null password cannot login"""
        self.reg_data['password'] = '    '
        self.login(code=400, msg='Enter Valid Data: Email and password')

    def test_login_missing_email(self):
        """Test user login with missing email"""
        del self.reg_data['email']
        self.login(code=422, msg='email should not be missing')

    def test_valid_json_request(self):
        """Test login request is json format"""
        del self.header['Content-Type']
        self.login(msg='Bad Request. Request should be JSON format', code=405)


class TestLogoutUser(BaseTestCase):
    """Test for Logout User endpoint"""
    def test_logout_user(self):
        """Test if logged in user can logout"""
        self.request_logic('/api/auth/logout',data=None, code=200,
                      msg='User Successfully logged out')



class TestResetPassword(BaseTestCase):
    """Test reset password user endpoint"""
    def reset_password(self, code, msg, data):
        self.request_logic('/api/auth/resetpassword', data=data,  code=code,
                      msg=msg)

    def test_password_reset(self):
        """Test password reset works as expected"""
        data = dict(email=self.reg_data['email'])
        self.reset_password(data=data, code=201,
                            msg='Check your email address for new password')

    def test_not_user_reset(self):
        """Test reset password with a non existing account"""
        data = {'email': 'non_reg@gmail.com'}
        self.reset_password(data=data, code=401,
                            msg='Invalid Email: Enter right credentions for reset password')

    def test_empty_user_reset(self):
        """Test reset password with an empty email"""
        data = {'email': '  '}
        self.reset_password(data=data, code=400,
                            msg='Enter Valid Email')

    def test_reset_missing_email(self):
        """Test reset password with a missing email address"""
        self.reset_password(data={}, code=422,
                            msg='email should not be missing')

    def test_valid_json_request(self):
        """Test reset password request is json format"""
        del self.header['Content-Type']
        data = dict(email=self.reg_data['email'])
        self.reset_password(msg='Bad Request. Request should be JSON format',
                                data=data, code=405)


class TestChangetPassword(BaseTestCase):
    """Test change password user endpoint"""
    def change_password(self, msg, code):
        self.request_logic('/api/auth/changepassword', data=self.passwords,
                      code=code, method='put', msg=msg)

    def test_password_change(self):
        """Test password change works as expected"""
        self.change_password(code=201, msg='Password Successfully Changed')

    def test_incorrect_initial_password(self):
        """Test password with incorrect old password input"""
        self.passwords['old_password'] = 'wrongpas'
        self.change_password(code=401, msg='Enter Valid Password: Old password is wrong')

    def test_empty_initial_password(self):
        """Test password with invalid password input"""
        self.passwords['old_password'] = '  '
        self.change_password(code=400, msg='Enter Valid Data: Email and password')

    def test_null_passwords(self):
        """Test password with invalid password input"""
        del self.passwords['old_password']
        self.change_password(code=422, msg='old_password should not be missing')

    def test_valid_json_request(self):
        """Test change password request is json format"""
        del self.header['Content-Type']
        self.change_password(msg='Bad Request. Request should be JSON format',
                                                         code=405)
