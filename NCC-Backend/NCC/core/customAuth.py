from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, ParseError

User = get_user_model()


class LeaderboardJwt(authentication.BaseAuthentication):
    '''Special authentication for leaderboard 
    if user is logged in user will get leaderboard with personal rank
    And if user is anonymous user will get leaderboard
    '''
    def authenticate(self, request):
        # Extract the JWT from the Authorization header
        jwt_token = request.META.get('HTTP_AUTHORIZATION')  #get token with Bearer
        if jwt_token is None:
            return None

        jwt_token = LeaderboardJwt.get_the_token_from_header(jwt_token)  # clean the token #get token without Bearer

        # Decode the JWT and verify its signature
        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed('Invalid signature')
        except:
            raise ParseError()

        # Get the user 
        userId = payload.get('user_id')
        if userId is None:
            raise AuthenticationFailed('User identifier not found in JWT')

        user = User.objects.filter(id=userId).first()   #to get user from id
        if user is None:
            user = User.objects.filter(id=userId).first()
            if user is None:
                raise AuthenticationFailed('User not found')

        # Return the user and token payload
        return user, payload

    def authenticate_header(self, request):
        return 'Bearer'

    @classmethod
    def get_the_token_from_header(cls, token):
        token = token.replace('Bearer', '').replace(' ', '')  # clean the token
        return token