from flask_app import app

from flask_app.models.vote import Vote

from flask import render_template, request, redirect, flash, session


from flask_app.models.user import User  # Import the User model



@app.route('/add_vote/<int:pie_id>', methods=['POST'])
def add_vote(pie_id):
    user_id = session.get('user_id')

    if not user_id:
        flash("Please log in to mark yourself as a vote.", 'vote_error')
        return redirect('/')

    # Check if the user is already voteal of this pie
    if Vote.has_user_voted(user_id, pie_id):
        flash("You are already voted this pie.", 'vote_error')
        return redirect(f"/show/{pie_id}")

    # Add the user to the list of votes for the pie
    Vote.create_vote({'user_id': user_id, 'pie_id': pie_id})
    flash("You let everyone know you voted this pie.", 'vote_success')
    return redirect(f"/show/{pie_id}")

@app.route('/remove_vote/<int:pie_id>', methods=['POST'])
def remove_vote(pie_id):
    if 'user_id' not in session:
        flash("Please log in to remove your vote.", 'remove_vote_error')
        return redirect('/')

    user_id = session['user_id']

    # Remove the user from the votes list
    Vote.remove_vote(user_id, pie_id)
    
    flash("You removed your vote because, tHiS PiE StInKs .", 'vote_success')
    return redirect(f'/show/{pie_id}')