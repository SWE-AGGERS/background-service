import unittest
from unittest import mock
from email_digest import send_emails

_app = None
 

class TestEmailSender(unittest.TestCase):
    def test_email_sender(self):
        with mock.patch('email_digest.get_all_stories_by_writer') as get_asbw_mock:
            with mock.patch('email_digest.get_followed_list') as get_fl_mock:
                with mock.patch('email_digest.get_user') as get_user_mock:
                    with mock.patch('email_digest.get_users') as get_users_mock:
                        get_asbw_mock.return_value = [0,0,0,0,0]
                        get_fl_mock.return_value = [1]
                        get_user_mock.return_value = { "user_id" : 3, "firstname": "Maurizio", "lastname": "Costanzo","email": "d.arioli@studenti.unipi.it","dateofbirth": ""},
                        get_users_mock.return_value = [{ "user_id" : 1, "firstname": "Tonio", "lastname": "Cartonio","email": "danimorpg@gmail.com","dateofbirth": ""},
                        { "user_id" : 2, "firstname": "Danilo", "lastname": "Numeroso","email": "ciao@example.it","dateofbirth": ""},
                        { "user_id" : 3, "firstname": "Maurizio", "lastname": "Costanzo","email": "d.arioli@studenti.unipi.it","dateofbirth": ""},
                        { "user_id" : 4, "firstname": "Ezio", "lastname": "Greggio","email": "intotheroom101@gmail.it","dateofbirth": ""},
                        { "user_id" : 5, "firstname": "Maria", "lastname": "Caterina","email": "danimorpg@gmail.com","dateofbirth": ""}]
                        self.assertTrue(send_emails())
