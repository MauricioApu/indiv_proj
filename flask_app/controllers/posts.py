from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.post import Post

@app.route('/post', methods=['post'])
def post():
    if not Post.validate(request.form):
        return redirect('/bright_ideas')
    data={
        "content": request.form['post'],
        "user_id": session['user_id']
    }
    Post.save(data)
    return redirect('/bright_ideas')

@app.route('/bright_ideas')
def bright_ideas():
    if 'user_id' in session:
        name=User.get_alias(session['user_id'])
        posts=Post.get_all()
        return render_template('dash.html', posts=posts,user=name[0]['alias'])
    else:
        flash('You must be logged in!')
        return redirect('/')
    
@app.route('/delete/<int:id>')
def delete(id):
    data={
        "post_id": id
    }
    check=Post.delete(data)
    if check:
        return redirect('/bright_ideas')
    else:
        flash("Couldn't delete post because you don't own it!")
        return redirect('/bright_ideas')
    
@app.route('/posts/<int:id>')
def onepost(id):
    if 'user_id' in session:
        data= {
            "post_id": id
        }
        posts=Post.get_one(data)
        name=User.get_alias(session['user_id'])
        likes=Post.get_likes(data)
        print(likes, 'aaaaaaaaaaaaaaaa')
        return render_template('post.html',post=posts, user=name[0]['alias'], likes=likes)
    else:
        flash('You must be logged in!')
        return redirect('/')
    

    
    