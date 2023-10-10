from utils.test import BaseSetup


# Create your tests here.
class SignupTestCase(BaseSetup):
    
    def test_user_signup(self):
        user_data = {
            "first_name": "string",
            "last_name": "string",
            "username": "mohamed_naser",
            "email": "mn9142001@gmail.com",
            "password1": "Mohamed13#",
            "password2": "Mohamed13#"
        }

        response = self.c.post('/user/auth/signup/', user_data, content_type="application/json")

        assert response.status_code != 200
