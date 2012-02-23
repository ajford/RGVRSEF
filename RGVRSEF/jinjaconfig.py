from re import compile as re_compile

from werkzeug import ImmutableDict

from . import app, utils

jinja_options = dict(app.jinja_options)
jinja_options.update({'trim_blocks':True})
app.jinja_options = ImmutableDict(jinja_options)

# Phone filter function for jinja
repl = lambda x: '-'.join([y for y in x if y is not None and y is not ''])
phoneRE = re_compile('([0-9]{3})?[^0-9]*([0-9]{3})[^0-9]*([0-9]{4})\Z')
prettyPhone = lambda x: repl(phoneRE.split(x))

def currency(x):
    try:
        return '$%.2f'%x
    except TypeError:
        return x

def nonone(x):
    if x is None:
        return ''
    else:
        return x

app.jinja_env.filters['phone']=prettyPhone
app.jinja_env.filters['currency']=currency
app.jinja_env.filters['nonone']=nonone
app.jinja_env.filters['encode']=utils.encode
app.jinja_env.add_extension('jinja2.ext.do')

