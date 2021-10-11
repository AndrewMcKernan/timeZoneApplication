import json
from django.contrib.auth.models import User
from django.urls import reverse
from .serializers import TimezoneSerializer
from .models import Timezone
from .views import *
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory, APIClient

class TimezoneTests(APITestCase):
    
    def setUp(self):
        new_user = User()
        new_user.username = "test"
        new_user.set_password("test")
        new_user.id = 1
        new_user.is_superuser = True
        new_user.save()
    
    def test_get_timezone(self):
        client = APIClient()
        
        request = client.post('/api/login', data={'username':'test', 'password':'test'})
        
        request = client.post('/api/timezone/', data={'name':'Test Name', 'city_name':'Edmonton', 'user':1}, format="json")
        
        request = client.get('/api/timezone/1/', headers={'Content-Type':'application/json'})
        self.assertEqual(request.json()['name'], 'Test Name')
        self.assertEqual(request.json()['city_name'], 'Edmonton')
        self.assertEqual(request.json()['user'], 1)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        
    def test_get_nonexistant_timezone(self):
        client = APIClient()
        
        request = client.post('/api/login', data={'username':'test', 'password':'test'})
        
        request = client.post('/api/timezone/', data={'name':'Test Name', 'city_name':'Edmonton', 'user':1}, format="json")
        
        request = client.get('/api/timezone/2/', headers={'Content-Type':'application/json'})
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_get_timezones(self):
        client = APIClient()
        
        request = client.post('/api/login', data={'username':'test', 'password':'test'})
        
        request = client.post('/api/timezone/', data={'name':'Test Name', 'city_name':'Edmonton', 'user':1}, format="json")
        request = client.post('/api/timezone/', data={'name':'Test Name 2', 'city_name':'Calgary', 'user':1}, format="json")
        request = client.get('/api/timezone/', headers={'Content-Type':'application/json'})
        self.assertEqual(len(request.json()), 2)
        
    
    def test_create_timezone(self):
        client = APIClient()
        
        request = client.post('/api/login', data={'username':'test', 'password':'test'})
        
        request = client.post('/api/timezone/', data={'name':'Test Name', 'city_name':'Edmonton', 'user':1}, format="json")
        
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        
        
    def test_create_timezone_no_info(self):
        client = APIClient()
        
        request = client.post('/api/login', data={'username':'test', 'password':'test'})
        
        request = client.post('/api/timezone/')
        
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        
        
    def test_create_timezone_incomplete_info(self):
        client = APIClient()
        
        request = client.post('/api/login', data={'username':'test', 'password':'test'})
        
        request = client.post('/api/timezone/', data={'city_name':'Edmonton', 'user':1}, format="json")
        
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_edit_timezone(self):
        client = APIClient()
        
        new_user = User()
        new_user.username = "test2"
        new_user.set_password("test2")
        new_user.id = 2
        new_user.is_superuser = True
        new_user.save()
        
        request = client.post('/api/login', data={'username':'test', 'password':'test'})
        
        client.post('/api/timezone/', data={'name':'Test Name', 'city_name':'Edmonton', 'user':1}, format="json")
        request = client.get('/api/timezone/1/', headers={'Content-Type':'application/json'})
        self.assertEqual(request.json()['name'], 'Test Name')
        self.assertEqual(request.json()['city_name'], 'Edmonton')
        self.assertEqual(request.json()['user'], 1)
        request = client.put('/api/timezone/1/', data={'id':1, 'name':'Test Name 2', 'city_name':'Calgary', 'user':2}, headers={'Content-Type':'application/json'})
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        request = client.get('/api/timezone/1/', headers={'Content-Type':'application/json'})
        self.assertEqual(request.json()['name'], 'Test Name 2')
        self.assertEqual(request.json()['city_name'], 'Calgary')
        self.assertEqual(request.json()['user'], 2)
        
    def test_edit_timezone_bad_request(self):
        client = APIClient()
        
        new_user = User()
        new_user.username = "test2"
        new_user.set_password("test2")
        new_user.id = 2
        new_user.is_superuser = True
        new_user.save()
        
        request = client.post('/api/login', data={'username':'test', 'password':'test'})
        
        client.post('/api/timezone/', data={'name':'Test Name', 'city_name':'Edmonton', 'user':1}, format="json")
        request = client.get('/api/timezone/1/', headers={'Content-Type':'application/json'})
        self.assertEqual(request.json()['name'], 'Test Name')
        self.assertEqual(request.json()['city_name'], 'Edmonton')
        self.assertEqual(request.json()['user'], 1)
        request = client.put('/api/timezone/1/', data={'id':1, 'name':'Test Name 2', 'city_name':'Calgary'}, headers={'Content-Type':'application/json'})
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_edit_timezone_nonexistant(self):
        client = APIClient()
        
        new_user = User()
        new_user.username = "test2"
        new_user.set_password("test2")
        new_user.id = 2
        new_user.is_superuser = True
        new_user.save()
        
        request = client.post('/api/login', data={'username':'test', 'password':'test'})
        
        client.post('/api/timezone/', data={'name':'Test Name', 'city_name':'Edmonton', 'user':1}, format="json")
        request = client.get('/api/timezone/1/', headers={'Content-Type':'application/json'})
        self.assertEqual(request.json()['name'], 'Test Name')
        self.assertEqual(request.json()['city_name'], 'Edmonton')
        self.assertEqual(request.json()['user'], 1)
        request = client.put('/api/timezone/3/', data={'id':1, 'name':'Test Name 2', 'city_name':'Calgary'}, headers={'Content-Type':'application/json'})
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_delete_timezone(self):
        client = APIClient()
        
        request = client.post('/api/login', data={'username':'test', 'password':'test'})
        
        request = client.post('/api/timezone/', data={'name':'Test Name', 'city_name':'Edmonton', 'user':1}, format="json")
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        request = client.delete('/api/timezone/1/')
        request = client.get('/api/timezone/1/', headers={'Content-Type':'application/json'})
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistant_timezone(self):
        client = APIClient()
        
        request = client.post('/api/login', data={'username':'test', 'password':'test'})
        
        request = client.post('/api/timezone/', data={'name':'Test Name', 'city_name':'Edmonton', 'user':1}, format="json")
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        request = client.delete('/api/timezone/2/')
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)
        request = client.get('/api/timezone/1/', headers={'Content-Type':'application/json'})
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        
        
class DecoratorTests(APITestCase):
    
    def setUp(self):
        new_user = User()
        new_user.username = "test"
        new_user.set_password("test")
        new_user.id = 1
        new_user.is_superuser = True
        new_user.save()
    
    def test_gmt_diff(self):
        client = APIClient()
        
        request = client.get('/api/timezone-info/Edmonton')
        # should be GMT -6
        self.assertEqual(request.json()['gmt_offset'], -6)
        
        request = client.get('/api/timezone-info/Ottawa')
        # should be GMT -4
        self.assertEqual(request.json()['gmt_offset'], -4)
        
    def test_gmt_error(self):
        client = APIClient()
        
        request = client.get('/api/timezone-info/Glorbaslorbablorb')
        # should be a 400
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(request.json(), "No location matches the inputted name.")
        
    def test_gmt_diff_between_cities(self):
        client = APIClient()
        
        request = client.get('/api/timezone-info/Edmonton/Moscow')
        # should be GMT -6
        self.assertEqual(request.json()['remote_gmt_offset'], 3)
        self.assertEqual(request.json()['local_gmt_offset'], -6)
        # 3 - (-6) is 9
        self.assertEqual(request.json()['offset_diff'], 9)
        # there are two more json items: "remote_city_timezone_now" and "local_city_timezone_now". We cannot test for the exact
        # correctness of the timestamp, since the server time is likely slightly different than the time the client has, and there
        # isn't really an easy way to synchronize that. 
        
        
class AccountTests(APITestCase):

    def setUp(self):
        new_user = User()
        new_user.username = "test"
        new_user.set_password("test")
        new_user.id = 1
        new_user.is_superuser = True
        new_user.save()

    def test_login(self):
        
        client = APIClient()
        
        request = client.post('/api/login', data={'username':'test', 'password':'test'})
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        
        request = client.post('/api/timezone/', data={'name':'Test Name', 'city_name':'Edmonton', 'user':1}, format="json")
        # this should be allowed
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        
    def test_login_fail(self):
        
        client = APIClient()

        request = client.post('/api/login', data={'username':'oops', 'password':'wrong'})
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)
        
        request = client.post('/api/timezone/', data={'name':'Test Name', 'city_name':'Edmonton', 'user':1}, format="json")
        # this should not be be allowed
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_get_own_id(self):
        
        client = APIClient()
        
        request = client.post('/api/login', data={'username':'test', 'password':'test'})
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        
        request = client.get('/api/user-id')
        # this should be allowed
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.json()['id'], 1)
        
    def test_logout(self):
        
        client = APIClient()
        
        request = client.post('/api/login', data={'username':'test', 'password':'test'})
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        
        request = client.post('/api/timezone/', data={'name':'Test Name', 'city_name':'Edmonton', 'user':1}, format="json")
        # this should be allowed
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        
        request = client.post('/api/logout')
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
        
        request = client.post('/api/timezone/', data={'name':'Test Name', 'city_name':'Edmonton', 'user':1}, format="json")
        # this should not be be allowed
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_registration(self):
        
        client = APIClient()
        
        request = client.post('/api/create-account', data={'username':'test2', 'password':'goodpasstime007', 'confirm-password':'goodpasstime007'})
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        
        request = client.post('/api/login', data={'username':'test2', 'password':'goodpasstime007'})
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        
    def test_create_superuser(self):
        
        client = APIClient()
        
        request = client.post('/api/login', data={'username':'test', 'password':'test'})
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        
        request = client.post('/api/create-account', data={'username':'superuser', 'password':'goodpasstime007', 'confirm-password':'goodpasstime007'})
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        
        request = client.post('/api/make-superuser/2/')
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        
        new_superuser = User.objects.get(username="superuser")
        self.assertEqual(new_superuser.is_superuser, True)
        
    def test_modify_own_permissions(self):
        
        client = APIClient()
        
        request = client.post('/api/login', data={'username':'test', 'password':'test'})
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        
        request = client.post('/api/make-superuser/1/')
        # should fail
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)
        
        new_superuser = User.objects.get(username="test")
        # should still be a superuser
        self.assertEqual(new_superuser.is_superuser, True)    
        
    def test_create_superuser_with_no_permissions(self):
        
        new_user = User()
        new_user.username = "test2"
        new_user.set_password("test2")
        new_user.id = 2
        new_user.is_superuser = False
        new_user.save()
        
        client = APIClient()
        
        request = client.post('/api/login', data={'username':'test2', 'password':'test2'})
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        
        request = client.post('/api/make-superuser/1/')
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)
        
        new_superuser = User.objects.get(username="test")
        # should be unchanged
        self.assertEqual(new_superuser.is_superuser, True)     
        
        
    def test_get_users_except_me(self):
        
        new_user = User()
        new_user.username = "test2"
        new_user.set_password("test2")
        new_user.id = 2
        new_user.is_superuser = False
        new_user.save()
        
        new_user = User()
        new_user.username = "test3"
        new_user.set_password("test3")
        new_user.id = 3
        new_user.is_superuser = False
        new_user.save()
        
        new_user = User()
        new_user.username = "test4"
        new_user.set_password("test4")
        new_user.id = 4
        new_user.is_superuser = False
        new_user.save()
        
        client = APIClient()
        
        request = client.post('/api/login', data={'username':'test', 'password':'test'})
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        request = client.get('/api/users')
        self.assertEqual(len(request.json()), 3)
        num = 2
        for user in request.json():
            self.assertEqual(user['username'], 'test' + str(num))
            self.assertEqual(user['id'], num)
            self.assertEqual(user['is_superuser'], False)
            num += 1
            
    def test_fail_get_users_except_me(self):
        
        new_user = User.objects.get(username="test")
        new_user.username = 'test1'
        new_user.set_password("test1")
        new_user.is_superuser = False
        new_user.save()
        
        new_user = User()
        new_user.username = "test2"
        new_user.set_password("test2")
        new_user.id = 2
        new_user.is_superuser = False
        new_user.save()
        
        new_user = User()
        new_user.username = "test3"
        new_user.set_password("test3")
        new_user.id = 3
        new_user.is_superuser = False
        new_user.save()
        
        new_user = User()
        new_user.username = "test4"
        new_user.set_password("test4")
        new_user.id = 4
        new_user.is_superuser = False
        new_user.save()
        
        client = APIClient()
        
        request = client.get('/api/users')
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_all_users(self):
        
        new_user = User.objects.get(username="test")
        new_user.username = 'test1'
        new_user.set_password("test1")
        new_user.is_superuser = True
        new_user.save()
        
        new_user = User()
        new_user.username = "test2"
        new_user.set_password("test2")
        new_user.id = 2
        new_user.is_superuser = True
        new_user.save()
        
        new_user = User()
        new_user.username = "test3"
        new_user.set_password("test3")
        new_user.id = 3
        new_user.is_superuser = True
        new_user.save()
        
        new_user = User()
        new_user.username = "test4"
        new_user.set_password("test4")
        new_user.id = 4
        new_user.is_superuser = True
        new_user.save()
        
        client = APIClient()
        
        request = client.post('/api/login', data={'username':'test1', 'password':'test1'})
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        request = client.get('/api/authors')
        self.assertEqual(len(request.json()), 4)
        num = 1
        for user in request.json():
            self.assertEqual(user['username'], 'test' + str(num))
            self.assertEqual(user['id'], num)
            self.assertEqual(user['is_superuser'], True)
            num += 1
            
    def test_fail_all_users(self):
        
        new_user = User.objects.get(username="test")
        new_user.username = 'test1'
        new_user.set_password("test1")
        new_user.is_superuser = False
        new_user.save()
        
        new_user = User()
        new_user.username = "test2"
        new_user.set_password("test2")
        new_user.id = 2
        new_user.is_superuser = True
        new_user.save()
        
        new_user = User()
        new_user.username = "test3"
        new_user.set_password("test3")
        new_user.id = 3
        new_user.is_superuser = True
        new_user.save()
        
        new_user = User()
        new_user.username = "test4"
        new_user.set_password("test4")
        new_user.id = 4
        new_user.is_superuser = True
        new_user.save()
        
        client = APIClient()
        
        request = client.post('/api/login', data={'username':'test1', 'password':'test1'})
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        request = client.get('/api/authors')
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)
        