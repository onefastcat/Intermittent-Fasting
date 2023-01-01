from flask import Blueprint, render_template, session, redirect, url_for, request
from app.meal_time_form import MealTime
from app.calculate_schedule import fastWindow, setFormValues
from datetime import time

bp = Blueprint('main', __name__)


@bp.route('/', methods=["GET", "POST"])
def main():


    print('--------------in main()-------------')
    form = MealTime()

    if('fastWindow' in session):
        print('fastWindow is in session')
        print(session['fastWindow'])



    #figure out where to initialize this. and what the valiues are first before form is submitted
    #msybe no need to initialize it here because I check for its existence in html
    # fastTimes = fastWindow(form)

    # if('fastTime' not in session):
    #     session['fastTime'] = fastWindow(form)
    #     print('added fasttime to session')

    #session['fastTime'] = fastWindow(form)

    if form.validate_on_submit():
        if not MealTime.mealGap(form, form.fastingHoursStart):
           message = 'Eating and fasting hours cannot exceed 24 hours'
           return redirect(url_for('main.timeConflict', message=message))

        #and MealTime.mealGap(form, form.minimumEatingWindow)
        #DEAL WITH THIS LATER

        #     return redirect(url_for('main.timeConflict'))

        print('---------form valid----------')



        if(fastWindow(form)):
            print('checks passed')

            print(session['fastWindow'])
            return redirect(url_for('main.main'))
        else:
            message = "This meal doesn't fit into the schedule"
            return redirect(url_for('main.timeConflict', message=message))
        #make sure you need to pass fastTimes here probably not. so i deleted it

        #session['minimumFastingWindow'] = form.minimumEatingWindow.data
        # session['originalFastWindow']['startFast'] = int(form.fastingHoursStart.data.strftime('%H'))
        # session['originalFastWindow']['endFast'] = int(form.fastingHoursEnd.data.strftime('%H'))



    else:
        # #maybe no need to do this conditional and put this under the next one about meals
        # if 'originalFastWindow' in session:
        #     print('//////////////////////')

        if('meals' in session):
            print('meals in session')
            setFormValues(form)
            print(session['meals'])
            return render_template('mealSchedule.html', form=form, fastTimes=session['fastWindow'], meals=session['meals'])
        #maybe no need to send fastTimes because I check for its existence in html
        return render_template('mealSchedule.html', form=form)



@bp.route('/mealtime-conflict')
def timeConflict():
    message = request.args.get('message')
    form = MealTime()
    return render_template('errorModal.html', form=form, message=message)
