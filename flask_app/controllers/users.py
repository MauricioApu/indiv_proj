from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
@app.route('/signin')
def signin():
    if 'user_id' in session:
        user=User.get_name_lname_email(session['user_id'])
        return render_template('dash.html', user=user)
    else:
        return render_template('login.html')
    
@app.route('/signup')
def signup():
    if 'user_id' in session:
        user=User.get_name(session['user_id'])
        return render_template('dash.html', user=user)
    else:
        return render_template('register.html')



@app.route('/register', methods=['post'])
def register():
    if not User.validate(request.form):
        return redirect('/signup')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    
    data = {
        "name": request.form["name"],
        "last_name" : request.form["last_name"],
        "email": request.form['email'],
        "password" : pw_hash
    }
    
    user_id = User.save(data)
    
    session['user_id'] = user_id
    return redirect('/bright_ideas')


@app.route('/login', methods=['POST'])
def login():
     
    data = {"email": request.form["email"]}
    user_in_db = User.get_by_email(data)
    
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/signin")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        
        flash("Invalid Email/Password")
        return redirect('/signin')
    
    session['user_id'] = user_in_db.id
    
    return redirect("/bright_ideas")

@app.route('/logout')
def clearsession():
    session.clear()
    return redirect('/')
    
@app.route('/users/<int:id>')
def profile(id):
    if 'user_id' in session:
        data= {
            "userid": id
        }
        name=User.get_alias(session['user_id'])
        numposts=User.get_numposts(data)
        numlikes=User.get_numlikes(data)
        data=User.get_name_lname_email(data)
        return render_template('profile.html',numposts=numposts, user=name[0]['alias'],numlikes=numlikes,data=data)
    else:
        flash('You must be logged in!')
        return redirect('/')
    
@app.route('/users/<int:id>/posts')
def posts(id):
    if 'user_id' in session:
        data= {
            "userid": id
        }
        posts=User.get_by_id(data)
        name=User.get_alias(session['user_id'])
        print(posts)
        return render_template('userideas.html',posts=posts, user=name[0]['alias'])
    else:
        flash('You must be logged in!')
        return redirect('/')