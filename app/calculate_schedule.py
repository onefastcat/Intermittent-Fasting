from flask import session
from datetime import time



def setFormValues(form):
    print('------------in setFormValues----------')
    form.fastingHoursEnd.data = time(session['originalFastWindow']['endFast'], 00, 00)
    form.fastingHoursStart.data = time(session['originalFastWindow']['startFast'], 00, 00)
    form.minimumEatingWindow.data = session['minimumEatingWindow']


def fastWindow(form):
    #test time. not real code

    print('--------------in calculate_schedule.py-------------')
    #this should be some type of initialization before form is submitted
    #runs when you open the page for the first time


    #maybe this is not needed now that i check for fastWindow existence inside html
    # if('fastWindow' not in session):
    #     print('no fastWindow in session from calculate_schedule.py')
    #     session['fastWindow'] = [
    #         {"day":"Monday","startFast":"24", "endFast": "0"},
    #         {"day":"Tuesday","startFast":"24", "endFast": "0"},
    #         {"day":"Wednesday","startFast":"24", "endFast": "0"},
    #         {"day":"Thursday","startFast":"24", "endFast": "0"},
    #         {"day":"Friday","startFast":"24", "endFast": "0"},
    #         {"day":"Saturday","startFast":"24", "endFast": "0"},
    #         {"day":"Sunday","startFast":"24", "endFast": "0"},
    #     ]
    #     return session['fastWindow']


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

        #must be updated if the values in the form are updated
        #and it does update because start and end values are taken from the form
        #-------------GO BACK TO THIS--------------------------------------------------
        session['originalFastWindow'] = {'startFast' : startTime,
                                         'endFast' : endTime}
        #------------------------------------------------------------------------------
        session['minimumEatingWindow'] = form.minimumEatingWindow.data


        if(recalcFastWindow(form)):
            return True
        #this loop recalculates each day fasting window based on the meals in session
        #maybe I on;y need it for the new incoming meal thats not in session yet
        # for meal in session['meals']:
        #     #recalculating fast window for next day
        #     if int(meal['timeOfMeal']) > startTime:
        #         print('------------------------!!!!!')
        #         for i in range(7):
        #             #session['fastWindow'][meal['dayOfMeal']]['startFast'] = int(meal['timeOfMeal'])+1
        #             if session['fastWindow'][i]['day'] == meal['dayOfMeal']:
        #                 addFastHours = int(meal['timeOfMeal']) - session['fastWindow'][i]['startFast'] + 1
        #                 session['fastWindow'][i]['startFast'] = int(meal['timeOfMeal'])+1
        #                 session['fastWindow'][i+1]['endFast'] += addFastHours
        #                 if session['fastWindow'][i+1]['startFast'] - session['fastWindow'][i+1]['endFast'] < int(session['minimumEatingWindow']):
        #                     return False
        #     # recalculating fast window for previous day
        #     if int(meal['timeOfMeal']) < endTime:
        #         for i in range(7):
        #             if(session['fastWindow'][i]['day'] == meal['dayOfMeal']):
        #                 print('---------------------------')
        #                 addFastHours = session['fastWindow'][i]['endFast'] - int(meal['timeOfMeal'])
        #                 session['fastWindow'][i]['endFast'] = int(meal['timeOfMeal'])
        #                 session['fastWindow'][i-1]['startFast'] -= addFastHours
        #                 if session['fastWindow'][i-1]['startFast'] - session['fastWindow'][i-1]['endFast'] < int(session['minimumEatingWindow']):
        #                     return False

        #                 print('---------------------------')


    #maybe no need to return this if I am useing session directly
    #maybe return True or false. because essentially this module calculates
    #the fasting window and determines if  it is valid
    return False

def validateMealTime(form):
    print('-------------in validateMealTime----------------')
    dayOfMeal = form.dayOfMeal.data
    timeOfMeal = int(form.timeOfMeal.data.strftime('%H'))
    for i in range(7):
        if session['fastWindow'][i]['day'] == dayOfMeal:
            if int(session['minimumEatingWindow']) > int(session['fastWindow'][i]['startFast']) - int(session['fastWindow'][i]['endFast']):
                 return False

    params = {
        'dayOfMeal' : form.dayOfMeal.data,
        'timeOfMeal' : form.timeOfMeal.data.strftime('%H')
    }

    if('meals' not in session):
        session['meals'] = []
    temp = session['meals']
    temp.append(params)
    session['meals'] = temp

    return True

def recalcFastWindow(form):
    print('-------------in recalcFastingWindow----------------')
    #recalculating fast window for next day
    startTime = int(form.fastingHoursStart.data.strftime('%H'))
    endTime = int(form.fastingHoursEnd.data.strftime('%H'))
    timeOfMeal = int(form.timeOfMeal.data.strftime('%H'))
    dayOfMeal = form.dayOfMeal.data

    if timeOfMeal > startTime:
        for i in range(7):
            if session['fastWindow'][i]['day'] == dayOfMeal:
                addFastHours = timeOfMeal - session['fastWindow'][i]['startFast'] + 1
                newFastStart = timeOfMeal+1
                newFastEnd = session['fastWindow'][i+1]['endFast'] + addFastHours
                if session['fastWindow'][i+1]['startFast'] - newFastEnd < int(session['minimumEatingWindow']):
                    return False
                else:
                    session['fastWindow'][i]['startFast'] = newFastStart
                    session['fastWindow'][i+1]['endFast'] = newFastEnd

            # recalculating fast window for previous day
    if timeOfMeal < endTime:
        for i in range(7):
            if session['fastWindow'][i]['day'] == dayOfMeal:
                addFastHours = session['fastWindow'][i]['endFast'] - timeOfMeal
                newFastStart = session['fastWindow'][i-1]['startFast'] - addFastHours
                newFastEnd = timeOfMeal
                if newFastStart - session['fastWindow'][i]['endFast'] < int(session['minimumEatingWindow']) \
                   or newFastStart - session['fastWindow'][i]['endFast'] < int(session['originalFastWindow']['startFast']) - int(session['originalFastWindow']['endFast']):
                    return False
                else:
                    session['fastWindow'][i]['endFast'] = newFastEnd
                    session['fastWindow'][i-1]['startFast'] = newFastStart


    #if all checks passed, add meal to session
    #maybe this should be a separate function
    validateMealTime(form)

    return True
