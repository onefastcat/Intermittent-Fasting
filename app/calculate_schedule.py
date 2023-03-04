from flask import session
from datetime import time


# set the following form values from previous submit
# these fields are less likely to be changed
# so they are pre-filled for user convenience
def setFormValues(form):
    form.fastingHoursEnd.data = time(session['originalFastWindow']['endFast'], 00, 00)
    form.fastingHoursStart.data = time(session['originalFastWindow']['startFast'], 00, 00)
    form.minimumEatingWindow.data = session['minimumEatingWindow']


def fastWindow(form):

    startTime = int(form.fastingHoursStart.data.strftime('%H'))
    endTime = int(form.fastingHoursEnd.data.strftime('%H'))

    if 'fastWindow' not in session:
        session['fastWindow'] = [
            {"day":"Monday", "startFast": startTime, "endFast": endTime},
            {"day":"Tuesday", "startFast": startTime, "endFast": endTime},
            {"day":"Wednesday", "startFast": startTime, "endFast": endTime},
            {"day":"Thursday", "startFast": startTime, "endFast": endTime},
            {"day":"Friday", "startFast": startTime, "endFast": endTime},
            {"day":"Saturday", "startFast": startTime, "endFast": endTime},
            {"day":"Sunday", "startFast": startTime, "endFast": endTime},
        ]

    # setting session object to keep track of beginning of fast and end of fast
    # after daily fast window is recalculated
    session['originalFastWindow'] = {'startFast' : startTime, 'endFast' : endTime}
    session['minimumEatingWindow'] = form.minimumEatingWindow.data

    if(validateMealTime(form) and checkEatingWindowConflict(form)):
        setSessionMeal(form)
        return True

    return False

# checks if new meal time generates conflict with other already existing meals
def validateMealTime(form):
    valid = True

    if('meals' in session):
        valid = checkMealConflict(form)

    return valid

def setSessionMeal(form):
    params = {
        'dayOfMeal' : form.dayOfMeal.data,
        'timeOfMeal' : form.timeOfMeal.data.strftime('%H')
    }

    if 'meals' not in session:
        session['meals'] = []

    temp = session['meals']
    temp.append(params)
    session['meals'] = temp

    return

# checks for conflict with existing meals
def checkMealConflict(form):
    dayOfMeal = form.dayOfMeal.data
    timeOfMeal = int(form.timeOfMeal.data.strftime('%H'))
    nextFastDay = findNextDay(dayOfMeal)
    prevFastDay = findPrevDay(dayOfMeal)
    prevDayMealList = list(filter(lambda meal: meal['dayOfMeal'] == prevFastDay['day'], session['meals']))
    nextDayMealList = list(filter(lambda meal: meal['dayOfMeal'] == nextFastDay['day'], session['meals']))
    originalFastDuration = int(session['originalFastWindow']['startFast']) - int(session['originalFastWindow']['endFast'])

    # find latest meal from previous day, if there isn't return an empty dictionary
    # which will be evaluated in the next conditional to False
    latestMeal = max(prevDayMealList, key=lambda x: x['timeOfMeal']) if prevDayMealList else {}
    earliestMeal = min(nextDayMealList, key=lambda x: x['timeOfMeal']) if nextDayMealList else {}

    # setting these meals to None since only the meals within one week are taken into account
    if dayOfMeal == "Monday":
        latestMeal = None
    if dayOfMeal == "Sunday":
        earliestMeal = None

    if (latestMeal and 24 - int(latestMeal['timeOfMeal']) + timeOfMeal - 1 < originalFastDuration):
        return False
    if (earliestMeal and 24 + int(earliestMeal['timeOfMeal']) - timeOfMeal - 1 < originalFastDuration):
        return False

    return True

def checkEatingWindowConflict(form):

    startTime = int(form.fastingHoursStart.data.strftime('%H'))
    endTime = int(form.fastingHoursEnd.data.strftime('%H'))
    timeOfMeal = int(form.timeOfMeal.data.strftime('%H'))

    if timeOfMeal >= startTime:
        no_conflict = validate_late_meal(form)
        if not no_conflict:
            return False
    elif timeOfMeal < endTime:
        no_conflict = validate_early_meal(form)
        if not no_conflict:
            return False

    return True

def validate_late_meal(form):
    dayOfMeal = form.dayOfMeal.data
    fastDay = list(filter(lambda day: day['day'] == dayOfMeal, session['fastWindow']))[0]
    timeOfMeal = int(form.timeOfMeal.data.strftime('%H'))
    nextFastDay = findNextDay(fastDay['day'])
    addFastHours = timeOfMeal - fastDay['startFast'] + 1

    if fastDay['day'] == 'Sunday':
        nextDayFastEnd = session['originalFastWindow']['endFast'] + addFastHours
        originalStartFast = session['originalFastWindow']['startFast']
    else:
        nextDayFastEnd = nextFastDay['endFast'] + addFastHours
        originalStartFast = nextFastDay['startFast']

    if originalStartFast - nextDayFastEnd < int(session['minimumEatingWindow']):
            return False

    if fastDay['day'] != 'Sunday':
        nextFastDay['endFast'] = nextDayFastEnd

    fastDay['startFast'] = max(timeOfMeal + 1, fastDay['startFast'])

    return True


def validate_early_meal(form):

    timeOfMeal = int(form.timeOfMeal.data.strftime('%H'))
    dayOfMeal = form.dayOfMeal.data
    fastDay = list(filter(lambda day: day['day'] == dayOfMeal, session['fastWindow']))[0]
    prevFastDay = findPrevDay(fastDay['day'])
    addFastHours_prevDay = fastDay['endFast'] - timeOfMeal

    if fastDay['day'] == 'Monday':
        prevDayFastEnd = session['originalFastWindow']['endFast']
        newFastStart_prevDay = session['originalFastWindow']['startFast'] - addFastHours_prevDay
    else:
        prevDayFastEnd = prevFastDay['endFast']
        newFastStart_prevDay = prevFastDay['startFast'] - addFastHours_prevDay

    if newFastStart_prevDay - prevDayFastEnd < int(session['minimumEatingWindow']):
        return False

    if fastDay['day'] != 'Monday':
        prevFastDay['startFast'] = min(newFastStart_prevDay, prevFastDay['startFast'])

    fastDay['endFast'] = min(timeOfMeal, fastDay['endFast'])

    return True


def findNextDay(day):
    if day == 'Monday':
        nextDay = 'Tuesday'
    elif day == 'Tuesday':
        nextDay = 'Wednesday'
    elif day == 'Wednesday':
        nextDay = 'Thursday'
    elif day == 'Thursday':
        nextDay = 'Friday'
    elif day == 'Friday':
        nextDay = 'Saturday'
    elif day == 'Saturday':
        nextDay = 'Sunday'
    else:
        nextDay = 'Monday'

    return list(filter(lambda day: day['day'] == nextDay, session['fastWindow']))[0]

def findPrevDay(day):
    if day == 'Monday':
        prevDay = 'Sunday'
    elif day == 'Tuesday':
        prevDay = 'Monday'
    elif day == 'Wednesday':
        prevDay = 'Tuesday'
    elif day == 'Thursday':
        prevDay = 'Wednesday'
    elif day == 'Friday':
        prevDay = 'Thursday'
    elif day == 'Saturday':
        prevDay = 'Friday'
    elif day == 'Sunday':
        prevDay = 'Saturday'
    else:
        raise Exception('day name not valid. provide valid day name')

    return list(filter(lambda day: day['day'] == prevDay, session['fastWindow']))[0]
