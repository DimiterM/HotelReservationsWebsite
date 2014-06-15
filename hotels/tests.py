from django.test import TestCase, Client

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from hotels.models import *


class SearchTest(TestCase):
    def setUp(self):
        t1 = Tag(tag='Tag1')
        t1.save()
        t2 = Tag(tag='Tag2')
        t2.save()
        t3 = Tag(tag='Tag3')
        t3.save()
        self.tags_ids = [t1.id, t2.id, t3.id]

        h1 = Hotel(name='Hilton', stars=5, location='Sofia, Bulgaria', text='!!!')
        h1.save()
        h1.tags.add(t1)
        h2 = Hotel(name='Sheraton', stars=5, location='Plovdiv, Bulgaria', text='!!!')
        h2.save()
        h2.tags.add(t1, t2)
        h3 = Hotel(name='Lazur', stars=3, location='Burgas, Bulgaria', text='!!!')
        h3.save()
        h3.tags.add(t1, t3)
        h4 = Hotel(name='Continental', stars=4, location='Varna, Bulgaria', text='!!!')
        h4.save()
        h4.tags.add(t1, t2, t3)
        h5 = Hotel(name='Belgrade', stars=3, location='Belgrade, Serbia', text='!!!')
        h5.save()
        h5.tags.add(t1, t3)
        

    def test_show_all(self):
        c = Client()
        response = c.get('/hotels/', {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['hotels_list']), 5)
        names = set(hotel.name for hotel in response.context['hotels_list'])
        self.assertEqual(names, set(['Hilton', 'Sheraton', 'Continental', 'Lazur', 'Belgrade']))

    def test_search_by_name_partial(self):
        c = Client()
        response = c.get('/hotels/', {'name': 'to', 'stars': 1, 'location': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['hotels_list']), 2)
        names = set(hotel.name for hotel in response.context['hotels_list'])
        self.assertEqual(names, set(['Hilton', 'Sheraton']))

    def test_search_multiple(self):
        c = Client()
        response = c.get('/hotels/', {'name': '', 'stars': 4, 'location': 'Bulg'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['hotels_list']), 3)
        names = set(hotel.name for hotel in response.context['hotels_list'])
        self.assertEqual(names, set(['Hilton', 'Sheraton', 'Continental']))
    
    def test_search_tags(self):
        c = Client()

        # if no tags are given
        response = c.get('/hotels/', {'name': '', 'stars': 1, 'location': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['hotels_list']), 5)
        names = set(hotel.name for hotel in response.context['hotels_list'])
        self.assertEqual(names, set(['Hilton', 'Sheraton', 'Continental', 'Lazur', 'Belgrade']))

        # if 1 tag is given
        response = c.get('/hotels/', {'name': '', 'stars': 1, 'location': '', 'tags': self.tags_ids[2]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['hotels_list']), 3)
        names = set(hotel.name for hotel in response.context['hotels_list'])
        self.assertEqual(names, set(['Continental', 'Lazur', 'Belgrade']))

        # if a combination of 2 tags is given
        response = c.get('/hotels/', {'name': '', 'stars': 1, 'location': '', 'tags': self.tags_ids[0], 'tags': self.tags_ids[1]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['hotels_list']), 2)
        names = set(hotel.name for hotel in response.context['hotels_list'])
        self.assertEqual(names, set(['Sheraton', 'Continental']))


class LoginTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user('tester', 'tester@email.com', 'testerpass')
        test_user.save()

    def test_wrong_pass(self):
        c = Client()
        response = c.post('/hotels/login/', {'username': 'tester', 'password': 'wrong'})
        self.assertEqual(response.status_code, 401)

    def test_correct_login(self):
        c = Client()
        response = c.post('/hotels/login/', {'username': 'tester', 'password': 'testerpass'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'tester')

    def test_logout(self):
        c = Client()
        response = c.get('/hotels/logout/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'AnonymousUser')

    def tearDown(self):
        test_user = User.objects.get(username='tester')
        test_user.delete()


class RegistrationTest(TestCase):
    def test_reg(self):
        c = Client()
        response = c.post('/hotels/register/', {'username': 'tester', 'email': 'tester@email.com', 'password1': 'testerpass', 'password2': 'testerpass', 'first_name': 'Test', 'last_name': 'User'})
        self.assertEqual(response.status_code, 200)
        
        db_entry = User.objects.get(username='tester', email='tester@email.com', first_name='Test', last_name='User')
        self.assertEqual(db_entry.username, 'tester')
        self.assertEqual(db_entry.email, 'tester@email.com')
        self.assertEqual(db_entry.first_name, 'Test')
        self.assertEqual(db_entry.last_name, 'User')

        login = self.client.login(username='tester',password='testerpass')
        self.assertTrue(login)

        test_user = User.objects.get(username='tester')
        test_user.delete()

    def test_cannot_reg_already_used_name(self):
        c = Client()
        response1 = c.post('/hotels/register/', {'username': 'tester', 'email': 'tester@email.com', 'password1': 'testerpass', 'password2': 'testerpass', 'first_name': 'Test', 'last_name': 'User'})
        self.assertEqual(response1.status_code, 200)

        response2 = c.post('/hotels/register/', {'username': 'tester', 'email': 'tester2@email.com', 'password1': 'testerpass2', 'password2': 'testerpass2', 'first_name': 'Test2', 'last_name': 'User2'})
        self.assertEqual(len(User.objects.filter(username='tester')), 1)

    def test_try_to_reg_with_different_passwords(self):
        c = Client()
        response = c.post('/hotels/register/', {'username': 'tester', 'email': 'tester@email.com', 'password1': 'testerpass', 'password2': 'different!', 'first_name': 'Test', 'last_name': 'User'})
        self.assertFalse(User.objects.filter(username='tester'))


class ReservationsTest(TestCase):
    def setUp(self):
        pass

    def test_successful_reservation(self):
        pass

    def test_not_enough_rooms(self):
        pass

    def test_optimal_scheduled(self):
        pass

    def tearDown(self):
        pass


class AlgorithmsTest(TestCase):
    def setUp(self):
        pass

    def test_get_free_rooms_of_type(self):
        pass

    def test_best_room_choice(self):
        pass

    def test_interval_partitioning(self):
        pass

    def tearDown(self):
        pass
