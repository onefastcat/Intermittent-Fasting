from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import InputRequired
from wtforms.fields import TimeField


class MealTime(FlaskForm):

    number_of_hours_choices = []
    day_choices = ['', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    for hour in range(0, 24):
        if(hour == 0):
            number_of_hours_choices.append('')
        else:
            number_of_hours_choices.append(hour)

    fastingHoursStart = TimeField("Start Fast", validators=[InputRequired()])
    fastingHoursEnd = TimeField("End Fast", validators=[InputRequired()])
    minimumEatingWindow = SelectField("Eating Window (hr)", choices=number_of_hours_choices, validators=[InputRequired()])
    dayOfMeal = SelectField("Meal Day",choices=day_choices, validators=[InputRequired()])
    timeOfMeal = TimeField("Meal Time", validators=[InputRequired()])
    submit = SubmitField("Calculate")

    def validate_minimumEatingWindow(form, minEatingWindow):
        startFast = int(form.fastingHoursStart.data.strftime('%H'))
        endFast = int(form.fastingHoursEnd.data.strftime('%H'))

        fastingHours = abs(endFast - startFast)
        eatingHours = int(form.minimumEatingWindow.data)

        #if eating hours and fasting hours exceed 24 hours return false
        if  eatingHours + fastingHours > 24:
            return False

        return True

    def validate_start(form, startTime):
        startFast = int(form.fastingHoursStart.data.strftime('%H'))
        endFast = int(form.fastingHoursEnd.data.strftime('%H'))

        if(startFast < endFast):
            print(startFast)
            print(endFast)
            return False

        return True
