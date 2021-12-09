from datetime import datetime
from datetime import timedelta
import jwt
from django.conf import settings

def generate_jwt_token(self):
    """
    Generates a JSON Web Token(JWT) for accessing the API.
    """
    dt = datetime.now() + timedelta(days=7)

    token = jwt.encode({
        'id': self.pk,
        'exp': dt
    }, settings.SECRET_KEY, algorithm='HS256')

    return token

