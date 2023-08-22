from flask_app import app


from flask import render_template, request, redirect, flash, session


from flask_app.models.tree import Tree
from flask_app.models.user import  User
from flask_app.models.visit import Visit
#Create
@app.route('/new/tree')
def new_tree():

    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/')

    user = User.get_one(user_id)
    if user is None:
        flash("User not found")
        return redirect('/')
    return render_template('new_tree.html', user=user )
@app.route('/create/tree', methods=["POST"])
def create_tree():
    if 'user_id' not in session:
        flash("Please log in to create_tree", 'tree_post_error')
        return redirect('/')
    
    data = {
        "user_id": session["user_id"],
        "species": request.form["species"],
        "location": request.form["location"],
        "reason": request.form["reason"],
        "date_planted": request.form["date_planted"]

    }

    if not Tree.validate_tree(data):
        return redirect("/new/tree")
    
    Tree.create_tree(data)
    flash("Tree planted", 'tree_plant_success')
    print('working')
    print(data)
    
    return redirect("/new/tree")
#read
@app.route('/show/<int:tree_id>', methods=['GET'])
def view_tree(tree_id):
    tree = Tree.get_tree_by_id_with_creator(tree_id)
    if not tree:
        flash("Tree not found.", 'view_tree_error')
        return redirect(f"/dashboard/{session['user_id']}")

    # Fetch the creator of the tree
    creator = tree.creator

    # Fetch the visits for the tree
    visits = Visit.get_users_visits_to_tree(tree_id)
    
    user_id = session['user_id']
    user = User.get_one(user_id)
    if user is None:
        flash("User not found")
        return redirect('/')
    
    return render_template('show_tree.html', tree=tree, session_user=session, creator=creator, visits=visits, user=user)


@app.route('/my_trees/<int:user_id>')
def my_trees(user_id):
    if 'user_id' not in session:
        flash("Please log in to view your trees.", 'my_trees_error')
        return redirect('/')

    user = User.get_one(user_id)
    if user is None:
        flash("User not found")
        return redirect('/')
    
    user_id = session['user_id']
    user_trees = Tree.get_trees_by_user_id(user_id)  # Replace with the appropriate method to get user's trees

    return render_template('my_trees.html',  user=user, user_trees=user_trees)



#edit tree

@app.route('/edit/<int:tree_id>', methods=['GET', 'POST'])
def edit_tree(tree_id):
    if 'user_id' not in session:
        flash("Please log in to edit a tree.", 'edit_tree_error')
        return redirect('/')

    user_id = session['user_id']
    user = User.get_one(user_id)
    if user is None:
        flash("User not found")
        return redirect('/')
    tree = Tree.get_tree_by_id_with_creator(tree_id)
    if tree is None:
        flash("Tree not found.", 'edit_tree_error')
        return redirect('/dashboard')

    if tree.user_id != session['user_id']:
        flash("You can only edit your own trees.", 'edit_tree_error')
        return redirect('/dashboard')

    if request.method == 'POST':
        data = {
            "id": tree_id,
            "user_id": session["user_id"],
            "species": request.form["species"],
            "location": request.form["location"],
            "reason": request.form["reason"],
            "date_planted": request.form["date_planted"],

        }

        if not tree.validate_tree(data):
            return redirect(f'/edit/{tree_id}')

        Tree.edit_tree(data)
        flash("Tree updated successfully.", 'edit_tree_success')
        return redirect(f"/edit/{tree_id}")

    return render_template('edit_tree.html', user=user, tree=tree)

# Delete
@app.route('/delete/<int:tree_id>', methods=['POST'])
def delete_tree(tree_id):
    if 'user_id' not in session:
        flash("Please log in to delete a tree.", 'delete_tree_error')
        return redirect('/')

    tree = Tree.get_tree_by_id_with_creator(tree_id)
    if not tree:
        flash("Tree not found.", 'delete_tree_error')
        return redirect(f"/dashboard/{session['user_id']}")

    if tree.user_id != session['user_id']:
        flash("You can only delete your own trees.", 'delete_tree_error')
        return redirect(f"/dashboard/{session['user_id']}")

    Tree.delete_tree(tree_id)
    flash("Tree deleted successfully.", 'delete_tree_success')
    return redirect(f"/my_trees/{session['user_id']}")

    
