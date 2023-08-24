from flask_app import app


from flask import render_template, request, redirect, flash, session


from flask_app.models.pie import Pie
from flask_app.models.user import  User
from flask_app.models.vote import Vote
#Create
@app.route('/pies')
def pie_rank():

    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/')

    user = User.get_one(user_id)
    if user is None:
        flash("User not found")
        return redirect('/')
    

    all_the_pies = Pie.get_all_pies_with_creator()  # Fetch all pies with their creators


    vote_counts = {}  # Dictionary to store vote counts for each pie

    for pie in all_the_pies:
        vote_counts[pie.id] = Vote.get_vote_count(pie.id)

    # Sort pies in descending order based on vote count
    sorted_pies = sorted(all_the_pies, key=lambda pie: vote_counts[pie.id], reverse=True)

    return render_template('pie_rank.html', user=user,  all_the_pies=all_the_pies, vote_counts=vote_counts, sorted_pies=sorted_pies )


@app.route('/create/pie', methods=["POST"])
def create_pie():
    if 'user_id' not in session:
        flash("Please log in to create_pie", 'pie_post_error')
        return redirect('/')
    
    data = {
        "user_id": session["user_id"],
        "name": request.form["name"],
        "filling": request.form["filling"],
        "crust": request.form["crust"]

    }

    if not Pie.validate_pie(data):
        return redirect(f"/dashboard/{session['user_id']}")
    
    Pie.create_pie(data)
    flash("Pie created", 'pie_created_successfully')
    print('working')
    print(data)
    
    return redirect(f"/dashboard/{session['user_id']}")
#read
@app.route('/show/<int:pie_id>', methods=['GET'])
def view_pie(pie_id):
    pie = Pie.get_pie_by_id_with_creator(pie_id)
    if not pie:
        flash("Pie not found.", 'view_pie_error')
        return redirect(f"/dashboard/{session['user_id']}")

    # Fetch the creator of the pie
    creator = pie.creator

    user_id = session['user_id']
    user = User.get_one(user_id)
    if user is None:
        flash("User not found")
        return redirect('/')
    votes = Vote.get_users_votes_to_pie(pie_id, user_id)

    user_has_voted = len(votes) > 0

    return render_template('show_pie.html', pie=pie, session_user=session, creator=creator, votes=votes, user=user, user_has_voted=user_has_voted)


# @app.route('/my_pies/<int:user_id>')
# def my_pies(user_id):
#     if 'user_id' not in session:
#         flash("Please log in to view your pies.", 'my_pies_error')
#         return redirect('/')

#     user = User.get_one(user_id)
#     if user is None:
#         flash("User not found")
#         return redirect('/')
    
#     user_id = session['user_id']
#     user_pies = Pie.get_pies_by_user_id(user_id)  # Replace with the appropriate method to get user's pies

#     return render_template('my_pies.html',  user=user, user_pies=user_pies)



#edit pie

@app.route('/edit/<int:pie_id>', methods=['GET', 'POST'])
def edit_pie(pie_id):
    if 'user_id' not in session:
        flash("Please log in to edit a pie.", 'edit_pie_error')
        return redirect('/')

    user_id = session['user_id']
    user = User.get_one(user_id)
    if user is None:
        flash("User not found")
        return redirect('/')
    pie = Pie.get_pie_by_id_with_creator(pie_id)
    if pie is None:
        flash("Pie not found.", 'edit_pie_error')
        return redirect(f"/dashboard/{session['user_id']}")

    if pie.user_id != session['user_id']:
        flash("You can only edit your own pies.", 'edit_pie_error')
        return redirect(f"/dashboard/{session['user_id']}")

    if request.method == 'POST':
        data = {
            "id": pie_id,
            "user_id": session["user_id"],
            "name": request.form["name"],
            "filling": request.form["filling"],
            "crust": request.form["crust"]

        }

        if not pie.validate_pie(data):
            return redirect(f'/edit/{pie_id}')

        Pie.edit_pie(data)
        flash("Pie updated successfully.", 'edit_pie_success')
        return redirect(f"/dashboard/{session['user_id']}")

    return render_template('edit_pie.html', user=user, pie=pie)

# Delete
@app.route('/delete/<int:pie_id>', methods=['POST'])
def delete_pie(pie_id):
    if 'user_id' not in session:
        flash("Please log in to delete a pie.", 'delete_pie_error')
        return redirect('/')

    pie = Pie.get_pie_by_id_with_creator(pie_id)
    if not pie:
        flash("Pie not found.", 'delete_pie_error')
        return redirect(f"/dashboard/{session['user_id']}")

    if pie.user_id != session['user_id']:
        flash("You can only delete your own pies.", 'delete_pie_error')
        return redirect(f"/dashboard/{session['user_id']}")

    Pie.delete_pie(pie_id)
    flash("Pie deleted successfully.", 'delete_pie_success')
    return redirect(f"/dashboard/{session['user_id']}")

    
