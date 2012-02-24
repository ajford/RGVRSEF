import base64

from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flask import session

from . import app
from . import exceptions

serializer = URLSafeTimedSerializer(app.config['SIGNING_KEY'])

SIG_EXPIRED = 'SIG_EXPIRED'
NOT_VIEWED = False
VIEWED = True
NOT_COMPLETE = False
COMPLETE = True 

def decode(x):
    """ Convenience function to decode Sponsor ID. """
    return base64.urlsafe_b64decode(str(x)+'='*(-len(x)%4))

def encode(x):
    """ Convenience function to encode Sponsor ID. """
    return base64.urlsafe_b64encode(str(x)).strip('=')


# Session tools
def store(**kwargs):
    """ Convenience function to sign and stash values in session."""
    for key in kwargs:
        try:
            session[key] = serializer.dumps(kwargs.get(key).serialize())
        except AttributeError: 
            session[key] = serializer.dumps(kwargs.get(key))

def retrieve(key):
    """ Convenience function to retrieved stashed values from session.
        Returns a dictionary containing keys passed in as args.
        """
    if session.has_key(key):
        return  serializer.loads(session.pop(key),
                    max_age=app.config['SIGNING_MAX_AGE'])
    else:
        app.logger.debug('Error retrieving %s - Not in Session'%key)
        raise exceptions.NoKeyError('%s does not exist'%key)

def refresh(key):
    """ Refreshes time stamp of a stashed value. """
    try:
        if session.has_key(key):
            session[key] = serializer.dumps(serializer.loads(session.pop(key),
                        max_age=app.config['SIGNING_MAX_AGE']))
            return True
        else:
            app.logger.debug('Error retrieving %s - Not in Session'%key)
            return False
    except SignatureExpired as expired:
        app.logger.warning('EXPIRED SIG - Error retrieving %s\n%s'%(key,
                                                                    expired))
        return False
    except BadSignature as badsig:
        app.logger.warning('BAD SIG - Error retrieving %s\n%s'%(key,badsig))
        return False

def clear():
    """ Clears session of all values. 

        WARNING: It is a 'dumb' clear, meaning it removes EVERYTHING, without
        discrimination. 
        """
    keys = session.keys()
    for key in keys:
        session.pop(key)

# Object Tools
def populate(dest,source):
    """ Copies values from source dict to destination object.
        Warning, this is a distructive operation, and will overwrite
        attribues of the destination object.
        """
    for key in source:
        dest.__setattr__(key,source[key])


def NYI():
    return render_template('message.html',message='Not Yet Implemented.')

