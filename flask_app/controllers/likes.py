from flask import redirect, session
from flask_app import app
from flask_app.models.like import Like

@app.route('/like/<int:id>')
def like(id):
    data={
        "post_id": id,
        "user_id": session['user_id']
    }
    Like.like(data)
    return redirect('/bright_ideas')

@app.route('/dislike/<int:id>')
def dislike(id):
    data={
        "post_id": id,
        "user_id": session['user_id']
    }
    Like.dislike(data)
    return redirect('/bright_ideas')