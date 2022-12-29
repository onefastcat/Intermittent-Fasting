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

        if(i < 10){
            newRow.innerText = `${i}:00 AM`;
           // newRow.id = `${i}-AM`;

        } else if(i > 12){
            newRow.innerText = `${i-12}:00 PM`;
            //newRow.id = `${i-12}-PM`;
        } else {
            newRow.innerText = `${i}:00 AM`;
            //newRow.id = `${i}-PM`;
        }
        if(i === 12){
            newRow.innerText = `12:00 PM`;
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

        if(i === 0){
            newTitleElement.innerText = '';
            newTitleElement.classList.remove('day');
            newTitleElement.classList.add('corner');
        }
        else if(i === 1) {
            newTitleElement.innerText = 'Monday';
        }
        else if(i === 2) {
            newTitleElement.innerText = 'Tuesday';
        }
        else if(i === 3) {
            newTitleElement.innerText = 'Wednesday';
        }
        else if(i === 4) {
            newTitleElement.innerText = 'Thurday';
        }
        else if(i === 5) {
            newTitleElement.innerText = 'Friday';
        }
        else if(i === 6) {
            newTitleElement.innerText = 'Saturday';
        }
        else if(i === 7) {
            newTitleElement.innerText = 'Sunday';
        }

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

}, false);



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


function mealTimeColor(mealsArr){

    let meals = JSON.parse(mealsArr);

    document.addEventListener('DOMContentLoaded', () => {

     for (let meal of meals){
         //console.log(meal['timeOfMeal']);
        // console.log(meal);
         let time = meal['timeOfMeal'];
         const day = meal['dayOfMeal'];
         if(time[0] == '0') {
            time = time.slice(1);
         }
         //console.log(time);

        const el = document.getElementById(time).getElementsByClassName(day)[0];

       // console.log(el)

        if(el){
            el.classList.add('meal')
        }

        }
    });
};




function fastWindowColor(fast){

    // const fastArr = fast.split(' ');
    // //check why index 0 gives empty space
    // const fastStart = fastArr[1];
    // const fastEnd = fastArr[2];
    // console.log('hi from js file');
    //need to convert the r3eceived JSON string into object,
    //so you use object methods on it
    const fastSchedule = JSON.parse(fast)
    // console.log(fastSchedule);

    //maybe this event listener should listen to form being submitted
    //insted of domcontentLoaded
    document.addEventListener('DOMContentLoaded', function() {

        console.log(fastSchedule)
        for(let i = 0; i < fastSchedule.length; i++) {

            let day = determineDayFromIndex(i);
            fastHour = document.getElementsByClassName(day)

            // console.log(fastHour);
            // console.log(fastSchedule[i]);
            // console.log(fastSchedule[i]['endFast']);
            for(let j = 0; j < fastSchedule[i]['endFast']; j++){
                fastHour[j].classList.add('fast');
                // console.log(fastHour[j])
            }
            for(let k = fastSchedule[i]['startFast']; k < 24; k++){
                fastHour[k].classList.add('fast');
                // console.log(fastHour[k])
            }
        }





    //  // console.log("here " +allHours.length)
    //   if(allHours){
    //   //  allHours.getElementsByClassName('data-cell').classList.add('red')
    //   //change later for 24 hour system instead of +12
    //   console.log(parseInt(fast.slice(0,3)))
    //     for(let item = fastStart; item < 24; item++){

    //         //this loop if I set fasting window on all days of the week
    //         for(let i = 0; i < 7; i++){
    //             allHours[item].children[i].classList.add('red')
    //         }



    //     }

    //     for(let item = 0; item <  fastEnd; item++){
    //         //this loop if I set fasting window on all days of the week
    //         for(let i = 0; i < 7; i++){
    //             allHours[item].children[i].classList.add('red')
    //         }


    //     }

    //   }


    });

}
