document.addEventListener('DOMContentLoaded', function() {
    var div = document.createElement('div');
    div.id = 'container2';
    div.innerText = 'Hi there!';
    div.className = 'border-pad';




    const parent = document.getElementsByClassName('table_head')[0];
    const tableBody = document.getElementsByClassName('table_body')[0];


    let tableHead = document.createElement('tr');
    tableHead.id = 'title';
    parent.appendChild(tableHead);

    for(let i = 0; i < 24; i++){
        let newRow = document.createElement('tr');
        newRow.classList.add('hour');

        if(i === 0) {
            newRow.innerText = `12:00 am`;
        }

        else if(i < 10){

            const inner = newRow.appendChild(document.createElement('div'));
            inner.classList.add('time_column');
            inner.innerText = `${i}:00 am`;

           // newRow.id = `${i}-AM`;

        } else if(i > 12){
            newRow.innerText = `${i-12}:00 pm`;
            //newRow.id = `${i-12}-PM`;
        } else {
            newRow.innerText = `${i}:00 am`;
            //newRow.id = `${i}-PM`;
        }
        if(i === 12){
            newRow.innerText = `12:00 pm`;
            //newRow.id = `12-PM`;
        }

        newRow.id = i;

        tableBody.appendChild(newRow);

    }


    const daysInAWeek = 7;

    for(let i = 0; i < daysInAWeek + 1; i++){
        let newTitleElement = document.createElement('th');
        newTitleElement.classList.add('day');
        tableHead = document.getElementById('title');
        tableHead.appendChild(newTitleElement);
        //---------------------figure this out.---------------

        setTableHeader(newTitleElement, i);


    }

    let hourElement = document.getElementsByClassName('hour');

    for (let row = 0; row < hourElement.length; row++){
        for(let i = 0; i < 7; i++){
            newData = document.createElement('td');
            newData.classList.add('data_cell');
            let className = determineDayFromIndex(i);
            newData.classList.add(className);
            hourElement[row].appendChild(newData);
        }
    }

    //document.getElementsByClassName('hour').appendChild(div);
   // const element = document.getElementsByClassName('container')[0];
    ///element.appendChild(div);
    //console.log(document.getElementsByClassName('container'));
    //console.log(element);


    const x = window.matchMedia("(min-width: 700px)");
    changeDayText(x);
    x.addEventListener('change', changeDayText);

}, false);




function changeDayText(x) {
    if (x.matches) { // If media query matches
        document.getElementById('Monday').innerText = 'Monday'
        document.getElementById('Tuesday').innerText = 'Tuesday'
        document.getElementById('Wednesday').innerText = 'Wednesday'
        document.getElementById('Thursday').innerText = 'Thursday'
        document.getElementById('Friday').innerText = 'Friday'
        document.getElementById('Saturday').innerText = 'Saturday'
        document.getElementById('Sunday').innerText = 'Sunday'
    } else {
        document.getElementById('Monday').innerText = 'M'
        document.getElementById('Tuesday').innerText = 'T'
        document.getElementById('Wednesday').innerText = 'W'
        document.getElementById('Thursday').innerText = 'T'
        document.getElementById('Friday').innerText = 'F'
        document.getElementById('Saturday').innerText = 'S'
        document.getElementById('Sunday').innerText = 'Sun'
    }
}



function determineDayFromIndex(i) {
    let day;
    if(i === 0) day = 'Monday';
            else if(i === 1) day = 'Tuesday';
            else if(i === 2) day = 'Wednesday';
            else if(i === 3) day = 'Thursday';
            else if(i === 4) day = 'Friday';
            else if(i === 5) day = 'Saturday';
            else day = 'Sunday';
    return day;
}


function mealTimeColor(mealsArr, fast){

    let meals = JSON.parse(mealsArr);
    let fasting = JSON.parse(fast);

    //if fasting is not array it's the originalFastWindow object, which means we are
    //showing previoud week view which doesn't have meals
    if(!Array.isArray(fasting)){
        // const el = document.getElementById('previous-week');
        // el.style = 'display: none;'

        return;
    }
    console.log("----------------meal  Color---------------------");
    document.addEventListener('DOMContentLoaded', () => {

     for (let meal of meals){

         let time = meal['timeOfMeal'];
         let day = meal['dayOfMeal'];
         if(time[0] == '0') {
            time = time.slice(1);
         }

        const el = document.getElementById(time).getElementsByClassName(day)[0];

        if(el){
            el.classList.add('meal')
        }

        }
    });
};




function fastWindowColor(fast, meals){


    const fastSchedule = JSON.parse(fast);
    const mealsList = JSON.parse(meals);
    console.log("----------------fast  Window  Color---------------------");
    console.log(fastSchedule)


    //if Fast schedule is not an array, it is a originalFastWindow
    // object that contains only startFast and endFast times

    if(!Array.isArray(fastSchedule)) {
        let startTime = fastSchedule['startFast'];
        let endTime = fastSchedule['endFast'];
        let sundayFastHoursStart = startTime;
        let mondayFastHoursEnd = endTime;



       //check if we are on /next-week url
        if (window.location.href.indexOf("next-week") > -1) {
            let latestMeal = findLatestMeal(mealsList);

            //change next week fast time only if the Sunday meal is late enough
            if(latestMeal['timeOfMeal'] > startTime){
                extraFastHours = latestMeal['timeOfMeal'] - startTime + 1;
                mondayFastHoursEnd = endTime + extraFastHours;
            }
        }
        //
        else if (window.location.href.indexOf("previous-week") > -1) {
            let earliestMeal = findEarliestMeal(mealsList);


            if(earliestMeal['timeOfMeal'] < endTime){
                extraFastHours = endTime - parseInt(earliestMeal['timeOfMeal']);
                sundayFastHoursStart = startTime - extraFastHours;
            }

        }

        document.addEventListener('DOMContentLoaded', function() {
           // console.log(fastSchedule)
            for(let i = 0; i < 7; i++) {
                let day = determineDayFromIndex(i);
                fastHour = document.getElementsByClassName(day)

                //sets early fastStart
                if(day === 'Sunday'){
                    startTime = sundayFastHoursStart;
                }
                //sets late fastEnd
                else if(day === 'Monday'){
                    endTime = mondayFastHoursEnd;
                }
                //resets endTime in case it is not applicable
                else {
                    endTime = fastSchedule['endFast'];
                }
                for(let j = 0; j < endTime; j++){
                    fastHour[j].classList.add('fast');
                }
                for(let k = startTime; k < 24; k++){
                    fastHour[k].classList.add('fast');

                }
            }


        });
    }

    //maybe this event listener should listen to form being submitted
    //insted of domcontentLoaded
    else{
        console.log('hereeeee')
        document.addEventListener('DOMContentLoaded', function() {
            for(let i = 0; i < 7; i++) {
             let day = determineDayFromIndex(i);
             fastHour = document.getElementsByClassName(day)
             //won't need to check if it is array because this loop is reused specifically for this. refactor later
                console.log(day)
                startTime = fastSchedule[i]['startFast'];
                endTime = fastSchedule[i]['endFast']

                for(let j = 0; j < endTime; j++){
                 fastHour[j].classList.add('fast');

                }
                for(let k = startTime; k < 24; k++){
                    fastHour[k].classList.add('fast');

                }


            }



            if(hasCertainDayMeal(mealsList, 'Sunday')){
                togglePrevNext('next');
            }
            if(hasCertainDayMeal(mealsList, 'Monday')){
                togglePrevNext('prev');
            }

        });

    }



}

function hasCertainDayMeal(meals, day){
    console.log('what is goin on')

    for(let meal of meals){

        if (meal['dayOfMeal'] == day){
            return true;
        }
    }

    return false;
}



function togglePrevNext(week){

    const corner = document.getElementsByClassName('corner')[0]
    lastWeek = corner.lastChild;
    nextWeek = corner.firstChild;
    console.log('togggggggling')
    console.log(nextWeek)
    if(week == 'next'){
        nextWeek.classList.remove('disabled');
    }
    else {
        lastWeek.classList.remove('disabled');
    }


}


function setTableHeader(element, i){


    if(i === 0){
        element.innerText = '';
        element.classList.remove('day');
        element.classList.add('corner');

        const queryString = window.location.search;
        const params = new URLSearchParams(queryString);
        const week = params.get('week');


         if (week === 'next') {

           element.innerHTML = "<a class='arrow previous' id='arrow_back' href='/'></a><a class='arrow next' id='arrow_forward' href='/?week=next'></a>";
           element.lastChild.classList.add('disabled');

         } else if (week === 'previous') {

            element.innerHTML = "<a class='arrow previous' id='arrow_back' href='/?week=previous'></a><a class='arrow next' id='arrow_forward' href='/'></a>"
            element.firstChild.classList.add('disabled');

        } else {

            element.innerHTML = "<a class='arrow next' id='arrow_forward' href='/?week=next'></a><a class='arrow previous' id='arrow_back' href='/?week=previous'></a>"
            element.firstChild.classList.add('disabled');
            element.lastChild.classList.add('disabled');

        }



    }
    else if(i === 1) {
        element.innerText = 'Monday';
        element.id = 'Monday';
    }
    else if(i === 2) {
        element.innerText = 'Tuesday';
        element.id = 'Tuesday';
    }
    else if(i === 3) {
        element.innerText = 'Wednesday';
        element.id = 'Wednesday';
    }
    else if(i === 4) {
        element.innerText = 'Thursday';
        element.id = 'Thursday';
    }
    else if(i === 5) {
        element.innerText = 'Friday';
        element.id = 'Friday';
    }
    else if(i === 6) {
        element.innerText = 'Saturday';
        element.id = 'Saturday';
    }
    else if(i === 7) {
        element.innerText = 'Sunday';
        element.id = 'Sunday';
    }
}


function findLatestMeal(mealsList){
    let latestMeal = mealsList[0];
    for(let meal of mealsList){
        if(meal['dayOfMeal'] === 'Sunday' && meal['timeOfMeal'] > latestMeal['timeOfMeal'])
        latestMeal = meal;
    }
    return latestMeal;
}

function findEarliestMeal(mealsList) {
    let earliestMeal = mealsList[0];
    for(let meal of mealsList) {
        if(meal['dayOfMeal'] === 'Monday' && meal['timeOfMeal'] < earliestMeal['timeOfMeal']){
            earliestMeal = meal;
        }
    }
    return earliestMeal;
}
