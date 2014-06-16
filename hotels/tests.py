from django.test import TestCase, Client

from django.contrib.auth import authenticate, login, logout
from datetime import date, timedelta
from django.contrib.auth.models import User

from hotels.models import *
from hotels.helper_views import *


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
        rt1 = RoomType(type='RoomType1')
        rt1.save()
        rt2 = RoomType(type='RoomType2')
        rt2.save()
        rt3 = RoomType(type='RoomType3')
        rt3.save()

        h = Hotel(name='TestHotel', stars=3, location='Test site', text='!!!')
        h.save()
        self.h_id = h.id

        self.r1 = Room(number=11, type=rt1, hotel=h)
        self.r1.save()
        self.r2 = Room(number=12, type=rt1, hotel=h)
        self.r2.save()
        self.r3 = Room(number=13, type=rt1, hotel=h)
        self.r3.save()

        self.r4 = Room(number=21, type=rt2, hotel=h)
        self.r4.save()

        self.r5 = Room(number=31, type=rt3, hotel=h)
        self.r5.save()

        self.test_user = User.objects.create_user('tester', 'tester@email.com', 'testerpass')
        self.test_user.save()

    def test_successful_reservation(self):
        c = Client()
        response = c.post('/hotels/login/', {'username': 'tester', 'password': 'testerpass'})
        response = c.post('/hotels/reserve/' + str(self.h_id) + '/', {'start_date': '2014-07-02', 'end_date': '2014-07-04', 'RoomType1':1, 'RoomType2':1, 'RoomType3':1})
        self.assertEqual(len(Reservation.objects.filter(start_date='2014-07-02', end_date='2014-07-04')), 3)


    def test_not_enough_rooms(self):
        c = Client()
        response = c.post('/hotels/login/', {'username': 'tester', 'password': 'testerpass'})

        response = c.post('/hotels/reserve/' + str(self.h_id) + '/', {'start_date': '2014-07-02', 'end_date': '2014-07-04', 'RoomType1': 1, 'RoomType2': 1, 'RoomType3': 1})
        previous_state = Reservation.objects.filter(start_date='2014-07-02', end_date='2014-07-04')

        c2 = Client()
        response2 = c2.post('/hotels/login/', {'username': 'tester', 'password': 'testerpass'})
        response2 = c2.post('/hotels/reserve/' + str(self.h_id) + '/', {'start_date': '2014-07-02', 'end_date': '2014-07-04', 'RoomType1': 2, 'RoomType2': 0, 'RoomType3': 1})
        self.assertEqual(response2.context['log'], "Not enough free rooms!")
        self.assertEqual(set(Reservation.objects.filter(start_date='2014-07-02', end_date='2014-07-04')), set(previous_state))

    def test_optimal_scheduled(self):
        c = Client()
        response = c.post('/hotels/login/', {'username': 'tester', 'password': 'testerpass'})

        res1 = Reservation(start_date='2014-07-02', end_date='2014-07-04', user=self.test_user, room=self.r1)
        res1.save()
        res2 = Reservation(start_date='2014-07-05', end_date='2014-07-06', user=self.test_user, room=self.r2)
        res2.save()
        res3 = Reservation(start_date='2014-07-07', end_date='2014-07-08', user=self.test_user, room=self.r2)
        res3.save()
        res4 = Reservation(start_date='2014-07-02', end_date='2014-07-05', user=self.test_user, room=self.r3)
        res4.save()
        res5 = Reservation(start_date='2014-07-06', end_date='2014-07-07', user=self.test_user, room=self.r3)
        res5.save()

        response = c.post('/hotels/reserve/' + str(self.h_id) + '/', {'start_date': '2014-07-01', 'end_date': '2014-07-06', 'RoomType1': 1, 'RoomType2': 0, 'RoomType3': 0})
        self.assertEqual(response.context['log'], "Success!")
        self.assertEqual(len(Reservation.objects.filter(start_date__gte='2014-07-01', end_date__lte='2014-07-08')), 6)

    def tearDown(self):
        Reservation.objects.all().delete()
        User.objects.get(username='tester').delete()



class AlgorithmsTest(TestCase):
    def setUp(self):
        rt1 = RoomType(type='RoomType1')
        rt1.save()
        rt2 = RoomType(type='RoomType2')
        rt2.save()

        h = Hotel(name='TestHotel', stars=3, location='Test site', text='!!!')
        h.save()
        self.h_id = h.id

        self.r1 = Room(number=11, type=rt1, hotel=h)
        self.r1.save()
        self.r2 = Room(number=12, type=rt1, hotel=h)
        self.r2.save()
        self.r3 = Room(number=13, type=rt1, hotel=h)
        self.r3.save()
        self.r4 = Room(number=21, type=rt2, hotel=h)
        self.r4.save()

        self.test_user = User.objects.create_user('tester', 'tester@email.com', 'testerpass')
        self.test_user.save()

    def test_get_free_rooms_of_type(self):
        c = Client()
        response = c.post('/hotels/login/', {'username': 'tester', 'password': 'testerpass'})
        response = c.post('/hotels/reserve/' + str(self.h_id) + '/', {'start_date': '2014-07-02', 'end_date': '2014-07-04', 'RoomType1': 2, 'RoomType2': 1})

        free_rooms = get_free_rooms_of_type(self.h_id, '2014-07-01', '2014-07-07', 'RoomType1')
        self.assertEqual(len(free_rooms), 1)

    def test_best_room_choice(self):
        c = Client()
        response = c.post('/hotels/login/', {'username': 'tester', 'password': 'testerpass'})

        res1 = Reservation(start_date='2014-07-02', end_date='2014-07-04', user=self.test_user, room=self.r1)
        res1.save()
        res2 = Reservation(start_date='2014-07-05', end_date='2014-07-06', user=self.test_user, room=self.r1)
        res2.save()
        res3 = Reservation(start_date='2014-07-02', end_date='2014-07-05', user=self.test_user, room=self.r2)
        res3.save()

        best_room = choose_best_room([self.r1, self.r2, self.r3], date(2014, 7, 7), date(2014, 7, 8))
        self.assertEqual(best_room, self.r1)

    def test_interval_partitioning(self):
        c = Client()
        response = c.post('/hotels/login/', {'username': 'tester', 'password': 'testerpass'})

        res1 = Reservation(start_date='2014-07-02', end_date='2014-07-04', user=self.test_user, room=self.r1)
        res1.save()
        res2 = Reservation(start_date='2014-07-05', end_date='2014-07-06', user=self.test_user, room=self.r2)
        res2.save()
        res3 = Reservation(start_date='2014-07-07', end_date='2014-07-08', user=self.test_user, room=self.r2)
        res3.save()
        res4 = Reservation(start_date='2014-07-02', end_date='2014-07-05', user=self.test_user, room=self.r3)
        res4.save()
        res5 = Reservation(start_date='2014-07-06', end_date='2014-07-07', user=self.test_user, room=self.r3)
        res5.save()

        result = interval_scheduling(self.h_id, 'RoomType1', '2014-07-01', '2014-07-06', self.test_user)
        self.assertTrue(result)
        self.assertEqual(len(Reservation.objects.filter(start_date__gte='2014-07-01', end_date__lte='2014-07-08')), 6)

        # assert conflicting reservations are assigned different rooms
        res1 = Reservation.objects.get(id=res1.id)
        res2 = Reservation.objects.get(id=res2.id)
        res3 = Reservation.objects.get(id=res3.id)
        res4 = Reservation.objects.get(id=res4.id)
        res5 = Reservation.objects.get(id=res5.id)
        res6 = Reservation.objects.get(start_date='2014-07-01', end_date='2014-07-06')

        self.assertNotEqual(res6.room.id, res2.room.id)
        self.assertNotEqual(res6.room.id, res4.room.id)
        self.assertNotEqual(res6.room.id, res1.room.id)
        self.assertNotEqual(res1.room.id, res4.room.id)
        self.assertNotEqual(res2.room.id, res5.room.id)
        self.assertNotEqual(res5.room.id, res6.room.id)
        self.assertNotEqual(res5.room.id, res3.room.id)

    def tearDown(self):
        Reservation.objects.all().delete()
        User.objects.get(username='tester').delete()
