#!flask/bin/python

from app import app
app.run(debug=True, host='127.0.0.1', port=9000)

"""
host='192.168.0.1',
port=80,
ssl_context=('cert.pem', 'key.pem')
)
"""