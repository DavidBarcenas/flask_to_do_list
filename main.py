import unittest
from flask import request, make_response, redirect, render_template, session
from flask_login import login_required, current_user

from app import create_app
from app.firestore_service import get_todos

app = create_app()

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip

    return response


@app.route('/hello')
@login_required
def hello():
    user_ip = session.get('user_ip')
    user_name = current_user.id

    context = {
        'user_ip': user_ip, 
        'user_name': user_name, 
        'todos': get_todos(user_name),
    }
    
    return render_template('hello.html', **context)