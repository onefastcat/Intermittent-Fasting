from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields import DateField, DateTimeLocalField, TimeField
from operator import attrgetter




class MealTime(FlaskForm):


    number_of_hours_choices = []
    # time_choices = []
    day_choices = ['', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    for hour in range(0, 24):
        if(hour == 0):
            number_of_hours_choices.append('')
        else:
            number_of_hours_choices.append(hour)


    def mealGap(form, field):
        print('here in MealGap')
        print(form.fastingHoursStart.data)
        fastingHours = 24 - int(form.fastingHoursStart.data.strftime('%H')) + int(form.fastingHoursEnd.data.strftime('%H'))
        eatingHours = int(form.minimumEatingWindow.data)
        if  eatingHours + fastingHours > 24:
            print('not valitd because of eating window')
            return False


        # if ('meals' in session) and len(session['meals']) > 0:

        #     latestMealTime = max(a['timeOfMeal'] for a in session['meals'])
        #     # stringTime = str(field.data)[0:2]

            #DEAL WITH THIS LATER
            # if 24 - int(latestMealTime) + int(stringTime) < int(form.fastingWindow.data):
            #      return False
        return True



    fastingHoursStart = TimeField("Start fasting at", validators=[DataRequired()])
    fastingHoursEnd = TimeField("Finish fasting at", validators=[DataRequired()])
    minimumEatingWindow = SelectField("Minimum eating window (hours) ", choices=number_of_hours_choices, validators=[DataRequired()])
    dayOfMeal = SelectField("Meal Day",choices=day_choices, validators=[DataRequired()])
    timeOfMeal = TimeField("Meal Time", validators=[DataRequired()])
    submit = SubmitField("Calculate")
