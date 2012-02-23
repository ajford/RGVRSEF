import base64

from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from . import app

serializer = URLSafeTimedSerializer(app.config['SIGNING_KEY'])
SIG_EXPIRED = 'SIG_EXPIRED'

def decode(x):
    """ Convenience function to decode Sponsor ID. """
    return base64.urlsafe_b64decode(str(x)+'='*(-len(x)%4))

def encode(x):
    """ Convenience function to encode Sponsor ID. """
    return base64.urlsafe_b64encode(str(x)).strip('=')

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
    try:
        if session.has_key(key):
            return  serializer.loads(session.pop(key),
                        max_age=app.config['SIGNING_MAX_AGE'])
        else:
            app.logger.debug('Error retrieving %s - Not in Session'%key)
            return None
    except SignatureExpired as expired:
        app.logger.warning('EXPIRED SIG - Error retrieving %s\n%s'%(key,
                                                                    expired))
        return SIG_EXPIRED
    except BadSignature as badsig:
        app.logger.warning('BAD SIG - Error retrieving %s\n%s'%(key,badsig))
        return None

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

def populate(dest,source):
    """ Copies values from source dict to destination object.
        Warning, this is a distructive operation, and will overwrite
        attribues of the destination object.
        """
    for key in source:
        dest.__setattr(key,source[key])

def NYI():
    return render_template('message.html',message='Not Yet Implemented.')

