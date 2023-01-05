from flask import Blueprint, render_template, session, redirect, url_for, request
from app.meal_time_form import MealTime
from app.calculate_schedule import fastWindow, setFormValues
from datetime import time

bp = Blueprint('main', __name__)


@bp.route('/', methods=["GET", "POST"])
def main():

    print('--------------in main()-------------')
    form = MealTime()

    #if reset button was clicked clear this session and
    if request.args.get('reset_btn') == 'reset':
        session.clear()
        return redirect(url_for('main.main'))

    if form.validate_on_submit():
        if not form.validate_minimumEatingWindow(form):
           message = 'Eating and fasting hours cannot exceed 24 hours.'
           session.clear()
           return redirect(url_for('main.timeConflict', message=message))
        if not form.validate_start(form):
            message = 'Fast start cannot be earlier than fast end.'
            session.clear()
            return redirect(url_for('main.timeConflict', message=message))

        print('---------form valid----------')

        if fastWindow(form):
            print('checks passed')

            return redirect(url_for('main.main'))
        else:
            message = "This meal doesn't fit into the schedule"
            return redirect(url_for('main.timeConflict', message=message))

    else:

        if('meals' in session):
            setFormValues(form)
            return render_template('mealSchedule.html', form=form, fastTimes=session['fastWindow'], meals=session['meals'])

        return render_template('mealSchedule.html', form=form)



@bp.route('/mealtime-conflict')
def timeConflict():
    message = request.args.get('message')
    form = MealTime()
    return render_template('errorModal.html', form=form, message=message)
