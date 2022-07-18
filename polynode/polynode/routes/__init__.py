"""
polynode.routes
~~~~~~~~~~~~~~~
Polynode's Base Route System.
"""
from flask import Blueprint

from .users import create_user, fetch_me

Users = Blueprint('users', 'polynode.routes.users')

Users.add_url_rule(
    '/<version>/register',
    'create_user',
    view_func=create_user.req,
    methods=['POST'],
    strict_slashes=False,
)
Users.add_url_rule(
    '/<version>/users/@me',
    'fetch_me',
    view_func=fetch_me.req,
    methods=['GET'],
    strict_slashes=False,
)
