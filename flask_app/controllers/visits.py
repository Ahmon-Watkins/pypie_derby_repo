from flask_app import app

from flask_app.models.visit import Visit

from flask import render_template, request, redirect, flash, session


from flask_app.models.user import User  # Import the User model



@app.route('/add_visit/<int:tree_id>', methods=['POST'])
def add_visit(tree_id):
    user_id = session.get('user_id')

    if not user_id:
        flash("Please log in to mark yourself as visital.", 'visit_error')
        return redirect('/')

    # Check if the user is already visital of this tree
    if Visit.has_user_visited(user_id, tree_id):
        flash("You are already visited this tree.", 'visit_error')
        return redirect(f"/show/{tree_id}")

    # Add the user to the list of visits for the tree
    Visit.create_visit({'user_id': user_id, 'tree_id': tree_id})
    flash("You let everyone know you visited this tree.", 'visit_success')
    return redirect(f"/show/{tree_id}")

@app.route('/remove_visit/<int:tree_id>', methods=['POST'])
def remove_visit(tree_id):
    if 'user_id' not in session:
        flash("Please log in to remove your visit.", 'remove_visit_error')
        return redirect('/')

    user_id = session['user_id']

    # Remove the user from the visits list
    Visit.remove_visit(user_id, tree_id)
    
    return redirect(f'/show/{tree_id}')