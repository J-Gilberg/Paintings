from flask_app import app
from flask_app.models import login_reg, painting
from flask import render_template, redirect, request, session, flash


@app.route('/dashboard')
def dashboard():
    if not 'user_id' in session:
        flash('Please log in to view this page')
        return redirect('/')
    
    purchases = painting.Painting.get_user_purchases({'id': session['user_id']})
    paintings = painting.Painting.get_all_paintings()
    user = login_reg.User.get_user({'id': session['user_id']})

    return render_template('dashboard.html', paintings = paintings, purchases = purchases, user = user)


# view
@app.route('/paintings/<int:painting_id>')
def view_painting(painting_id):
    if not 'user_id' in session:
        flash('Please log in to view this page')
        return redirect('/')
    single_painting = painting.Painting.get_painting({'id': painting_id})
    return render_template("view_painting.html", painting = single_painting)


# create
@app.route('/paintings/new')
def new_painting():
    if not 'user_id' in session:
        flash('Please log in to view this page')
        return redirect('/')
    return render_template('new_painting.html')


@app.route('/addpainting', methods=['POST'])
def add_painting():
    if not 'user_id' in session:
        flash('Please log in to view this page')
        return redirect('/')
    if not painting.Painting.painting_validator(request.form):
        return redirect('/paintings/new')
    painting.Painting.add_painting(request.form)
    return redirect('/dashboard')


# delete
@app.route('/deletepainting/<int:painting_id>')
def delete_painting(painting_id):
    if not 'user_id' in session:
        flash('Please log in to view this page')
        return redirect('/')
    single_painting = painting.Painting.get_painting({'id': painting_id})
    if single_painting.user_id != session['user_id']:
        flash('Please log in to view this page')
        return redirect('/')
    painting.Painting.delete_painting({'id': painting_id})
    return redirect('/dashboard')


# edit
@app.route('/paintings/<int:painting_id>/edit')
def edit_painting(painting_id):
    if not 'user_id' in session:
        flash('Please log in to view this page')
        return redirect('/')
    single_painting = painting.Painting.get_painting({'id': painting_id})
    if single_painting.user_id != session['user_id']:
        flash('Please log in to view this page')
        return redirect('/')
    return render_template('edit_painting.html', painting = single_painting)


@app.route('/editpainting/<int:painting_id>', methods=['POST'])
def update_painting(painting_id):
    if not 'user_id' in session:
        flash('Please log in to view this page')
        return redirect('/')
    if not painting.Painting.painting_validator(request.form):
        return redirect(f'/paintings/{painting_id}/edit')
    painting.Painting.edit_painting(request.form)
    return redirect('/dashboard')

@app.route('/buypainting/<int:painting_id>')
def buy_painting(painting_id):
    if not 'user_id' in session:
        flash('Please log in to view this page')
        return redirect('/')
    painting.Painting.add_purchase({'painting_id': painting_id, 'user_id': session['user_id']})
    return redirect('/dashboard')