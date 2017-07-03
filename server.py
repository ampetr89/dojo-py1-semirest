from flask import Flask, render_template, redirect, request
from mysqlconnection import MySQLConnection
from datetime import datetime as dt

app = Flask(__name__)
app.secret_key = open('secret_key.txt', 'r').read().strip()
db = MySQLConnection(app, 'semirestful')

def fmt_ts(ts):
	return ts.strftime('%B %d %Y, %I:%M %p')

@app.route('/')
def root():
	return redirect('/users')

@app.route('/users')
def index():
	users= db.query_db('select id, first_name, last_name, email, created_at \
	 from users order by created_at')
	for user in users:
		user['created_at'] = fmt_ts(user['created_at'])

	return render_template('index.html', users=users)

@app.route('/users/<userid>', methods=['GET', 'POST'])
def show(userid):
	if request.method == 'GET':
		query = 'select id, first_name, last_name, email, created_at \
		from users where id=:id'
		user = db.query_db(query, {'id': userid})[0]
		user['created_at'] = fmt_ts(user['created_at'])
		return render_template('show.html', user=user)

	else:
		data = {
				'first_name': request.form['first_name'],
				'last_name': request.form['last_name'],
				'email': request.form['email']
			}
		db.query_db('update users set \
			first_name = :first_name, \
			last_name = :last_name, \
			email = :email', data)

		return redirect('/users/'+str(userid))


@app.route('/users/<userid>/edit')
def edit(userid):
	query = 'select id, first_name, last_name, email \
		from users where id=:id'
	user = db.query_db(query, {'id': userid})[0]
	return render_template('edit.html', user=user)

@app.route('/users/new')
def new():
	return render_template('new.html')

@app.route('/users/create', methods=['POST'])
def create():
	data = {
		'first_name': request.form['first_name'],
		'last_name': request.form['last_name'],
		'email': request.form['email']
	}
	query = 'insert into users (first_name, last_name, email) \
	values(:first_name, :last_name, :email)'
	newid =  db.query_db(query, data)

	return redirect('/users/'+str(newid))


@app.route('/users/<userid>/destroy')
def destroy(userid):
	query = 'delete from users where id=:id'
	db.query_db(query, {'id': userid})
	return redirect('/users')


app.run(debug=True)