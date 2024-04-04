from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.recipe import recipe_class
from flask_app.models.accounts import accounts_class
from flask import flash


@app.route('/welcome')
def helloname():
    if 'accounts_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['accounts_id']
    }
    return render_template("myrecipes.html",  accounts_class=accounts_class.get_by_id(data),recipes=recipe_class.get_all())

@app.route('/recipe/new')
def create_recipe():
    if 'accounts_id' not in session:
        return redirect('/logout')

    return render_template('newrecipe.html')

@app.route('/recipe/new/process', methods=['POST'])
def process_recipe():
    if 'accounts_id' not in session:
        return redirect('logout')
    if not recipe_class.validate_recipe(request.form):
        return redirect('/recipe/new')

    data = {
        'accounts_id': session['accounts_id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'under30': request.form['under30'],
    }
    recipe_class.save(data)
    print()
    return redirect('/welcome')

@app.route('/recipes/<int:id>')
def view_recipe(id):
    if 'accounts_id' not in session:
        return redirect('/logout')

    return render_template('viewrecipe.html',recipe=recipe_class.get_by_id({'id': id}))

@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    if 'accounts_id' not in session:
        return redirect('/logout')

    recipe_class.delete({'id':id})
    return redirect('/welcome')

@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if 'accounts_id' not in session:
        return redirect('/logout')

    return render_template('editrecipe.html',recipe=recipe_class.get_by_id({'id': id}))

@app.route('/recipes/edit/process/<int:id>', methods=['POST'])
def process_edit_recipe(id):
    if 'accounts_id' not in session:
        return redirect('/logout')
    if not recipe_class.validate_recipe(request.form):
        return redirect(f'/recipes/edit/{id}')
    data = {
        'id': id,
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'under_30': request.form['under30'],
    }
    recipe_class.update(data)
    return redirect('/welcome')




@staticmethod
def validate_recipe(form_data):
        is_valid = True

        if len(form_data['name']) < 3:
            flash("Name must be at least 3 characters long.")
            is_valid = False
        if len(form_data['description']) < 3:
            flash("Description must be at least 3 characters long.")
            is_valid = False
        if len(form_data['instructions']) < 3:
            flash("Instructions must be at least 3 characters long.")
            is_valid = False
        if form_data['date_made'] == '':
            flash("Please input a date.")
            is_valid = False
        if 'under30' not in form_data:
            flash("Give me cook time.")
            is_valid = False

        return is_valid