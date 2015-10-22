from firstapp import app
from flask import Flask, render_template, request, flash, session, redirect, url_for
from forms import SignupForm, SigninForm, DeleteForm, ModifyForm
#from flask.ext.mail import Message, Mail
from models import db, User 

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()
 
  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      return 'Form posted.'
 
  elif request.method == 'GET':
    return render_template('contact.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()
  
  if 'username' in session:
    return redirect(url_for('profile'))

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = User(form.username.data, form.homefolder.data, form.shelltype.data, form.sudopr.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()   

      session['username'] = newuser.username
      return redirect(url_for('profile'))
   
  elif request.method == 'GET':
    return render_template('signup.html', form=form)

@app.route('/profile')
def profile():

  form = DeleteForm()
  form1 = ModifyForm()

  if 'username' not in session:
    return redirect(url_for('signin'))
 
  user = User.query.filter_by(username = session['username']).first()
 
  if user is None:
    return redirect(url_for('signin'))
  else:
    return render_template('profile.html', user=user, form=form, form1=form1)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()
  
  if 'username' in session:
    return redirect(url_for('profile'))

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signin.html', form=form)
    else:
      session['username'] = form.username.data
      return redirect(url_for('profile'))
                 
  elif request.method == 'GET':
    return render_template('signin.html', form=form)

@app.route('/signout')
def signout():
 
  if 'username' not in session:
    return redirect(url_for('signin'))
     
  session.pop('username', None)
  return redirect(url_for('home'))

@app.route('/delete', methods=['GET', 'POST'])
def delete():
  form = SigninForm()

  if request.method == 'POST':
    user = User.query.filter_by(username = session['username']).first()
    db.session.delete(user)
    db.session.commit()
    session.pop('username', None)
  return render_template('delete.html',form=form)

@app.route('/modify', methods=['GET', 'POST'])
def modify():
  form = ModifyForm()
  
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('modify.html', form=form)
    else:
      user_mod = User.query.filter_by(username = session['username']).first()
      #user_mod = User(form.username.data, form.homefolder.data, form.shelltype.data, form.sudopr.data)
      #user_mod.username = form.username.data
      user_mod.homefolder = form.homefolder.data
      user_mod.shelltype = form.shelltype.data
      user_mod.sudopr = form.sudopr.data
      db.session.commit()
    return redirect(url_for('profile'))
  
@app.route('/testdb')
def testdb():
  if db.session.query("1").from_statement("SELECT 1").all():
    return 'It works.'
  else:
    return 'Something is broken.'