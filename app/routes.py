from flask import Blueprint, render_template, session, redirect, url_for
from app.meal_time_form import MealTime
from app.calculate_schedule import fastWindow

bp = Blueprint('main', __name__)


@bp.route('/', methods=["GET", "POST"])
def main():


    print('--------------in main()-------------')
    form = MealTime()
    if 'meals' in session:
        form = MealTime()

    #figure out where to initialize this. and what the valiues are first before form is submitted
    #msybe no need to initialize it here because I check for its existence in html
    # fastTimes = fastWindow(form)

    # if('fastTime' not in session):
    #     session['fastTime'] = fastWindow(form)
    #     print('added fasttime to session')

    #session['fastTime'] = fastWindow(form)

    if form.validate_on_submit():
        #and MealTime.mealGap(form, form.minimumEatingWindow)
        #DEAL WITH THIS LATER

        #     return redirect(url_for('main.timeConflict'))

        print('form validated from routes')

        if('meals' not in session):
            session['meals'] = []

        params = {
            #move the commented out parts into another session variable.

            #'fastingHoursStart': form.fastingHoursStart.data.strftime('%H'),
            #'fastingHoursEnd': form.fastingHoursEnd.data.strftime('%H'),
            #'minimumEatingWindow': form.minimumEatingWindow.data,
            'dayOfMeal' : form.dayOfMeal.data,
            'timeOfMeal' : form.timeOfMeal.data.strftime('%H')
        }

        if(len(session['meals']) > 0):
            temp = session['meals']
            temp.append(params)
            session['meals'] = temp
           # print(' added element to session list ')
           # print(session['meals'])
        else:
           # print('ever here')
            session['meals'].append(params)
        #print(session['fastWindow'])
        fastTimes = fastWindow(form)
        #make sure you need to pass fastTimes here probably not. so i deleted it
        return redirect(url_for('main.main'))
    else:
        if('meals' in session):
            print('meals in session')
            return render_template('mealSchedule.html', form=form, fastTimes=session['fastWindow'], meals=session['meals'])
        #maybe no need to send fastTimes because I check for its existence in html
        return render_template('mealSchedule.html', form=form)



@bp.route('/mealtime-conflict')
def timeConflict():
    form = MealTime()
    return render_template('errorModal.html', form=form)
