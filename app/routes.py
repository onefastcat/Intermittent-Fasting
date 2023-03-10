from flask import Blueprint, render_template, session, redirect, url_for, request, flash, get_flashed_messages
from app.meal_time_form import MealTime
from app.calculate_schedule import fastWindow, setFormValues

bp = Blueprint('main', __name__)


@bp.route('/', methods=["GET", "POST"])
def main():

    form = MealTime()

    if request.method == 'GET':
        if request.args.get('week') == 'next' or request.args.get('week') == 'previous':
            setFormValues(form)
            return render_template('mealSchedule.html',form=form, fastTimes=session['originalFastWindow'], meals=session['meals'])


    if form.validate_on_submit():
        if not form.validate_minimumEatingWindow(form):
            flash('Eating and fasting hours cannot exceed 24 hours.', category='error')
            get_flashed_messages(with_categories=True)
        #    session.clear()
            if('meals' in session):
                return render_template('mealSchedule.html', form=form, fastTimes=session['fastWindow'], meals=session['meals'] )
            return render_template('mealSchedule.html', form=form)
        elif not form.validate_start(form):
            flash('Fast start cannot be earlier than fast end', category='error')
            get_flashed_messages(with_categories=True)
            # session.clear()

            if('meals' in session):
                return render_template('mealSchedule.html', form=form, fastTimes=session['fastWindow'], meals=session['meals'] )
            return render_template('mealSchedule.html', form=form)

        # if all checks pass
        # return the home page
        # fastWindow checks the validty of new meal time
        if fastWindow(form):
            return redirect(url_for('main.main'))

        else:
            flash("This meal doesn't fit into the schedule", category='error')
            get_flashed_messages(with_categories=True)
            if('meals' in session):
                return render_template('mealSchedule.html', form=form, fastTimes=session['fastWindow'], meals=session['meals'] )
            return render_template('mealSchedule.html', form=form)

    else:

        if('meals' in session):
            setFormValues(form)
            return render_template('mealSchedule.html', form=form, fastTimes=session['fastWindow'], meals=session['meals'])

        return render_template('mealSchedule.html', form=form, meals=[])


@bp.route('/clear')
def reset():
    session.clear()
    return redirect(url_for('main.main'))
