from flask import session
from datetime import time



# set the following form values from previous submit
# these fields are less likely to be changed
# so they are pre-filled for user convenience
def setFormValues(form):
    print('------------in setFormValues----------')
    form.fastingHoursEnd.data = time(session['originalFastWindow']['endFast'], 00, 00)
    form.fastingHoursStart.data = time(session['originalFastWindow']['startFast'], 00, 00)
    form.minimumEatingWindow.data = session['minimumEatingWindow']


def fastWindow(form):
    #test time. not real code

    print('--------------in calculate_schedule.py-------------')

    #I don't like this conditional here. maybe need to check it in the routes.py
    if form.fastingHoursStart.data:

        startTime = int(form.fastingHoursStart.data.strftime('%H'))
        endTime = int(form.fastingHoursEnd.data.strftime('%H'))



        if 'fastWindow' not in session:
            session['fastWindow'] = [
                {"day":"Monday", "startFast": startTime, "endFast": endTime},
                {"day":"Tuesday", "startFast":startTime, "endFast": endTime},
                {"day":"Wednesday", "startFast":startTime, "endFast": endTime},
                {"day":"Thursday", "startFast":startTime, "endFast": endTime},
                {"day":"Friday", "startFast":startTime, "endFast": endTime},
                {"day":"Saturday", "startFast":startTime, "endFast": endTime},
                {"day":"Sunday", "startFast":startTime, "endFast": endTime},
             ]

        print('---------------------fastingHours initialized------------------')


        # setting session object to keep track of beginning of fast and end of fast
        # even after daily fast window is recalculated
        session['originalFastWindow'] = {'startFast' : startTime,
                                         'endFast' : endTime}
        #------------------------------------------------------------------------------
        # setting session object to keep track of minimum eating hours in a day
        session['minimumEatingWindow'] = form.minimumEatingWindow.data


        if(validateMealTime(form) and recalcFastWindow(form)):
            setSessionMeal(form)
            return True

    return False

def validateMealTime(form):
    print('-------------in validateMealTime----------------')
    dayOfMeal = form.dayOfMeal.data
    timeOfMeal = int(form.timeOfMeal.data.strftime('%H'))
    #extract the relevant day where meal is to be placed
    fastDay = list(filter(lambda day: day['day'] == dayOfMeal, session['fastWindow']))[0]
    nextFastDay = findNextDay(dayOfMeal)
    prevFastDay = findPrevDay(dayOfMeal)

    if('meals' in session):
        prevDayMealList = list(filter(lambda meal: meal['dayOfMeal'] == prevFastDay['day'], session['meals']))
        nextDayMealList = list(filter(lambda meal: meal['dayOfMeal'] == nextFastDay['day'], session['meals']))
        originalFastDuration = int(session['originalFastWindow']['startFast']) - int(session['originalFastWindow']['endFast'])

        # find latest meal from previous day, if there isn't return an empty dictionary
        # which will be evaluated in the next conditional to False
        latestMeal = max(prevDayMealList, key=lambda x: x['timeOfMeal']) if prevDayMealList else {}
        earliestMeal = min(nextDayMealList, key=lambda x: x['timeOfMeal']) if nextDayMealList else {}

        if (latestMeal and 24 - int(latestMeal['timeOfMeal']) + timeOfMeal - 1 <
            originalFastDuration):
                print('calculates back to previoous day')
                return False
        if (earliestMeal and int(earliestMeal['timeOfMeal']) + 24 - timeOfMeal - 1 <
            originalFastDuration):
                print('calculating forward to next day')
                return False

    return True

def setSessionMeal(form):
    params = {
        'dayOfMeal' : form.dayOfMeal.data,
        'timeOfMeal' : form.timeOfMeal.data.strftime('%H')
    }

    if('meals' not in session):
        session['meals'] = []
    temp = session['meals']
    temp.append(params)
    session['meals'] = temp

    return

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
        #deal with this later. figure out what type of exception to raise
        raise Exception('day name not valid. provide valid day name')

    return list(filter(lambda day: day['day'] == prevDay, session['fastWindow']))[0]


def recalcFastWindow(form):
    print('-------------in recalcFastingWindow----------------')
    #recalculating fast window for next day
    originalFastDuration = int(session['originalFastWindow']['startFast']) - int(session['originalFastWindow']['endFast'])
    startTime = int(form.fastingHoursStart.data.strftime('%H'))
    endTime = int(form.fastingHoursEnd.data.strftime('%H'))
    timeOfMeal = int(form.timeOfMeal.data.strftime('%H'))
    dayOfMeal = form.dayOfMeal.data
    fastDay = list(filter(lambda day: day['day'] == dayOfMeal, session['fastWindow']))[0]
    nextFastDay = findNextDay(fastDay['day'])
    prevFastDay = findPrevDay(fastDay['day'])


    #THIS CHECK isnt meant to WORK IF SOMEONE EATS AT NIGHT AND FASTS DURING DAYtime
    if timeOfMeal >= startTime:

        addFastHours = timeOfMeal - fastDay['startFast'] + 1
        newFastStart = timeOfMeal+1
        if fastDay['day'] != 'Sunday':
                    newFastEnd = nextFastDay['endFast'] + addFastHours
        else:
            newFastEnd = session['originalFastWindow']['endFast'] + addFastHours

        if fastDay['day'] == 'Sunday':
            if session['originalFastWindow']['startFast'] - newFastEnd < int(session['minimumEatingWindow']):
                return False
            fastDay['startFast'] = newFastStart
        elif fastDay['day'] != 'Sunday':
            if nextFastDay['startFast'] - newFastEnd < int(session['minimumEatingWindow']):
                return False
            fastDay['startFast'] = newFastStart
            nextFastDay['endFast'] = newFastEnd

    # recalculating fast window for previous day
    if timeOfMeal < endTime:
        addFastHours = fastDay['endFast'] - timeOfMeal

        #why is thjis here??
        if('meals' in session):

            prevDayMeal = dict(filter(lambda meal: meal['dayOfMeal'] == prevFastDay, session['meals']))
            print(prevDayMeal)
            #what is this??????
            #this functionality is not done yet. it recalcs fasting hours and makes conflict with\
            #existing meals schedules the day before here and day after in the code above
            #take care of this
            if('timeOfMeal' in prevDayMeal):

                if prevDayMeal['timeOfMeal'] >= session['originalFastWindow']['startFast']:
                    print('prevDay meal exists and time is later than original fast')
                    return False
                newFastStart = max(prevFastDay['startFast'] - addFastHours, int(prevDayMeal['timeOfMeal']))
            else:
                newFastStart = prevFastDay['startFast'] - addFastHours
        else:
            newFastStart = prevFastDay['startFast'] - addFastHours

        newFastEnd = timeOfMeal
                #what is this?
        if newFastStart - prevFastDay['endFast'] < int(session['minimumEatingWindow']) \
            or abs(newFastStart + timeOfMeal)< originalFastDuration:
            return False
        else:
             #check if day is other than Monday. if it is, don't set previous day fastWidnow
            if fastDay['day'] != 'Monday':
                fastDay['endFast'] = newFastEnd
                prevFastDay['startFast'] -=  addFastHours
            else:
                fastDay['endFast'] = newFastEnd

    return True
