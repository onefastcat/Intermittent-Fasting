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


        if(recalcFastWindow(form) and validateMealTime(form)):
            setSessionMeal(form)
            return True

    return False

def validateMealTime(form):
    print('-------------in validateMealTime----------------')
    dayOfMeal = form.dayOfMeal.data
    timeOfMeal = int(form.timeOfMeal.data.strftime('%H'))

    for i in range(7):
        if session['fastWindow'][i]['day'] == dayOfMeal:
            print(session['fastWindow'][i]['startFast'])
            print(session['originalFastWindow']['startFast'])
            if (session['fastWindow'][i]['endFast'] > session['originalFastWindow']['endFast'] and
                timeOfMeal < session['fastWindow'][i]['endFast']):
                    print('should place a new meal')
                    return False
            if (session['fastWindow'][i]['startFast'] < session['originalFastWindow']['startFast'] and
                timeOfMeal >= session['fastWindow'][i]['startFast']):
                    print('meal to late')
                    return False
            if int(session['minimumEatingWindow']) > int(session['fastWindow'][i]['startFast']) - int(session['fastWindow'][i]['endFast']):
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


def indexToDay(i):
    #figure out how to handle meals set for Monday which produces index -1

    if i == 0:
        return 'Monday'
    elif i == 1:
        return 'Tuesday'
    elif i == 2:
        return 'Wednesday'
    elif i == 3:
        return 'Thursday'
    elif i == 4:
        return 'Friday'
    elif i == 5:
        return 'Saturday'
    #temporary solution
    elif i == 6 or i == -1:
        return 'Sunday'
    else:
        raise Exception("index provided is not valid. must be in the range(0,7)")

def recalcFastWindow(form):
    print('-------------in recalcFastingWindow----------------')
    #recalculating fast window for next day
    originalFastDuration = int(session['originalFastWindow']['startFast']) - int(session['originalFastWindow']['endFast'])
    startTime = int(form.fastingHoursStart.data.strftime('%H'))
    endTime = int(form.fastingHoursEnd.data.strftime('%H'))
    timeOfMeal = int(form.timeOfMeal.data.strftime('%H'))
    dayOfMeal = form.dayOfMeal.data


    #MAYBE SOME PARTS OF THESE TWO HUGE CONDITIONALS BELONG IN VALIDATE MEAL TIME
    #THIS CHECK DOESNT WORK IF SOMEONE EATS AT TNIGHT AND FASTS DURING DAYtime
    if timeOfMeal >= startTime and startTime > endTime:
        for i in range(7):
            if session['fastWindow'][i]['day'] == dayOfMeal:
                #figure out what to to if day is Sunday
                #introducing j as 0 is a temp solution
                # this makes Monday of this week the next day
                # in a circular fashion
                if i == 6:
                    j = 0
                addFastHours = timeOfMeal - session['fastWindow'][i]['startFast'] + 1

                newFastStart = timeOfMeal+1
                newFastEnd = session['fastWindow'][j]['endFast'] + addFastHours
                if session['fastWindow'][j]['startFast'] - newFastEnd < int(session['minimumEatingWindow']):
                    return False
                else:
                    session['fastWindow'][i]['startFast'] = newFastStart
                    session['fastWindow'][j]['endFast'] = newFastEnd

            # recalculating fast window for previous day
    if timeOfMeal < endTime and startTime > endTime:
        for i in range(7):
            if session['fastWindow'][i]['day'] == dayOfMeal:
                addFastHours = session['fastWindow'][i]['endFast'] - timeOfMeal

                   #new fast start hour for previous day
                if('meals' in session):
                    prevDay = indexToDay(i-1)
                    prevDayMeal = dict(filter(lambda meal: meal['dayOfMeal'] == prevDay, session['meals']))
                    #what is this??????
                    #this functionality is not done yet. it recalcs fasting hours and makes conflict with\
                    #existing meals schedules the day before here and day after in the code above
                    #take care of this
                    if('timeOfMeal' in prevDayMeal):
                        print('prevDayMeal prevents new meal')
                        newFastStart = max(session['fastWindow'][i-1]['startFast'] - addFastHours, int(prevDayMeal['timeOfMeal']))
                    else:
                        newFastStart = session['fastWindow'][i-1]['startFast'] - addFastHours
                else:
                    newFastStart = session['fastWindow'][i-1]['startFast'] - addFastHours
                newFastEnd = timeOfMeal
                #what is this?
                if newFastStart - session['fastWindow'][i-1]['endFast'] < int(session['minimumEatingWindow']) \
                   or abs(newFastStart + timeOfMeal)< originalFastDuration:
                    return False
                else:
                    session['fastWindow'][i]['endFast'] = newFastEnd
                    session['fastWindow'][i-1]['startFast'] = newFastStart

    return True
