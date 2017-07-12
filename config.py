WTF_CSRF_ENABLED = True
SECRET_KEY = 'qs!832djer90@2jhs290weoc+-c'

OPENID_PROVIDERS = [
	{'name' : 'Google', 'url' : 'https://www.google.com/accounts/o8/id'},
	{'name' : 'Yahoo', 'url' : 'https://me.yahoo.com/'},
	{'name' : 'AOL', 'url' : 'https://openid.aol.com/<username>'},
	{'name' : 'Flicker', 'url' : 'http://www.flicker.com/<username>'},
	{'name' : 'MyOpenID', 'url' : 'https://www.myopenid.com'}
]

# Database
SQLALCHEMY_TRACK_MODIFICATIONS = False

