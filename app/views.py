import re, json
from flask import render_template, redirect, flash, request, jsonify
from app import app

from .forms import InputForm
from .forms import LoginForm


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
			# {  "emails": { "user": "Ashik" }}

			try :
				content = json.dumps(json.loads(content), indent=int(data['indent']), sort_keys=True)
				content = content.replace('\r\n', '')
			except:
				pass

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
