from flask import session


def fastWindow(form):
    #test time. not real code

    print('--------------in calculate_schedule.py-------------')

    print(form.fastingHoursStart.data)
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



    if form.fastingHoursStart.data and ('meals' in session):
        print('fastingHours set------------------')
        startTime = int(form.fastingHoursStart.data.strftime('%H'))
        endTime = int(form.fastingHoursEnd.data.strftime('%H'))

        session['fastWindow'] = [
            {"day":"Monday", "startFast": startTime, "endFast": endTime},
            {"day":"Tuesday", "startFast":startTime, "endFast": endTime},
            {"day":"Wednesday", "startFast":startTime, "endFast": endTime},
            {"day":"Thursday", "startFast":startTime, "endFast": endTime},
            {"day":"Friday", "startFast":startTime, "endFast": endTime},
            {"day":"Saturday", "startFast":startTime, "endFast": endTime},
            {"day":"Sunday", "startFast":startTime, "endFast": endTime},
        ]

        for meal in session['meals']:
           # print(endTime)
            print('recalculating fasting window')
            print(session['meals'])
            #recalculating fast window for next day
            if int(meal['timeOfMeal']) > startTime:
                print('------------------------!!!!!')
                for i in range(7):
                    #session['fastWindow'][meal['dayOfMeal']]['startFast'] = int(meal['timeOfMeal'])+1
                    if session['fastWindow'][i]['day'] == meal['dayOfMeal']:
                        addFastHours = int(meal['timeOfMeal']) - session['fastWindow'][i]['startFast'] + 1
                        session['fastWindow'][i]['startFast'] = int(meal['timeOfMeal'])+1
                        session['fastWindow'][i+1]['endFast'] += addFastHours
            # recalculating fast window for previous day
            if int(meal['timeOfMeal']) < endTime:
                for i in range(7):
                    if(session['fastWindow'][i]['day'] == meal['dayOfMeal']):
                        print('---------------------------')
                        addFastHours = session['fastWindow'][i]['endFast'] - int(meal['timeOfMeal'])
                        session['fastWindow'][i]['endFast'] = int(meal['timeOfMeal'])
                        session['fastWindow'][i-1]['startFast'] -= addFastHours

                        print('---------------------------')



    return session['fastWindow']
