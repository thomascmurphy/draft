from flask import current_app

from .models import *

class User():
    #methods
    @staticmethod
    def get_user_by_email(email):
      user = select_first_item('users', ["email='%s'" % email])
      return user

    @staticmethod
    def create_user(email, pin):
      user = insert_item('users', {'email': email, 'pin': pin})
      return user

    @staticmethod
    def update_user(values, params):
        users_update = update_item('users', values, params)
        user = select_first_item('users', params)
        return user

    @staticmethod
    def update_user_by_id(id, values):
        return User.update_user(values, ["users.id=%i" % id])


