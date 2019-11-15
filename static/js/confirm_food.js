"use strict";

const updateMeal = () => {

    const dateInput = new Date($('#time_eaten').val());


    if (dateInput.getHours() < 14 && dateInput.getHours() > 11) {
        $('#meal_to_add').val('2');
    }

    // if timeEaten is between 6am and 9am -> value of meal = breakfast
    // if timeEaten is between 11:00am and 1:30 pm -> valeu of meal = lunch
    // if timeEaten is between 5:30pm and 9:00pm -> value of meal = dinner
    // ELSE value of meal = snack
}


const timeInput = document.querySelector('#time_eaten');

timeInput.addEventListener('change', updateMeal)
  // alert('You should be updating the meal!');

  
