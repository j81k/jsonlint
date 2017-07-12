import re, json
from flask import render_template, redirect, flash, request, jsonify
from app import app

from .forms import InputForm
from .forms import LoginForm

def dict_raise_on_duplicates(ordered_pairs):
    """Reject duplicate keys."""
    d = {}
    for k, v in ordered_pairs:
        if k in d:
           raise ValueError("Duplicate key is found: %r" % (k,))
        else:
           d[k] = v
    return d

def dict_allow_on_duplicates(ordered_pairs):
	d = {}
	index = 0
	for k, v in ordered_pairs:
		index += 1
		if k in d:
			d[k+'--DUPLICATE--'+str(index)] = v
		else:
			d[k] = v	

	return d	

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	data = {
		'logged' : True,
		#'logged' : False,
		'user' : {
			'name' : 'Guest'
		},

		'indent' : 4,
		'indents' : [2, 4, 6, 8, 12]

	}
	
	if not data['logged']:
		return redirect('/login')

	data['form'] = InputForm()	
	if data['form'].validate_on_submit():
		# Validate Json
		import demjson

		data['message'] = {
			'type' : 'success',
			'text' : 'Valid JSON!',
		}
		content = data['form'].json_inp.data.strip()
		data['indent'] = request.form.get('stats_tab_select')

		try :
			# {"data": {"name": "Ui","user": "Assk","user": "kio"}}

			try :
				if data['form'].duplicate_key.data :
					content = json.loads(content, object_pairs_hook=dict_raise_on_duplicates)
				else :
					content = json.loads(content, object_pairs_hook=dict_allow_on_duplicates)
					
				content = json.dumps(content, indent=int(data['indent']), sort_keys=True)
				content = content.replace('\r\n', '')
			except ValueError as e:
				#pass
				content = content.replace('\n', '')
				text = str(e).replace('\n', '')
				data['message']['type'] = 'error'
				data['message']['text'] = text.replace('u\'', '\'')

			demjson.decode(content, strict=True)
			content = content.replace('\n','\r\n') #'&#13;&#10;') 

		except demjson.JSONDecodeError, error:
			text = error.pretty_description().replace('\n', '')
			
			#regex = re.compile(': (.*?): (.*?): u(.*?) +\| +At line (\d+), column (\d+)', re.IGNORECASE)
			regex = re.compile(': (.*?): (.*?) +\| +At line (\d+), column (\d+),', re.IGNORECASE)
			for m in re.findall(regex, text):
				data['message']['type'] = m[0].lower()
				data['message']['text'] = m[1].replace('u\'', '\'')
				data['message']['line'] = m[2]
				data['message']['column'] = m[3]

				#flash(m[0] + ': '+m[1].replace('u\'', '\''))
				#flash('Line: ' + m[2])
				#flash('Word at: '+ m[2])
				#flash('Column: '+ m[3])
				
		data['json_inp'] = content
			
	return render_template('index.html', data=data)


	   
@app.errorhandler(Exception)
def unhandled_exception(e):
    return jsonify('Unhandled Exception: %s', (e))
    #return redirect('/')
	
	

	
@app.route('/login', methods=['GET', 'POST'])
def login():
	data = {
		'form' : LoginForm(),
		'providers' : app.config['OPENID_PROVIDERS']
	}

	if data['form'].validate_on_submit():
		flash('Login requested for Open ID="%s", remember_me=%s' % 
				(data['form'].openid.data, str(data['form'].remember_me.data))
			)
		return redirect('/index')
	
	return render_template('login.html', data=data)
