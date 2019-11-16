"use strict";

const updateMeal = () => {

    const dateInput = new Date($('#time_eaten').val());

    // if timeEaten is between 6am and 9am -> value of meal = breakfast
    // if timeEaten is between 11:00am and 1:30 pm -> valeu of meal = lunch
    // if timeEaten is between 5:30pm and 9:00pm -> value of meal = dinner
    // ELSE value of meal = snack

    if (dateInput.getHours() > 6 && dateInput.getHours() < 9) {
        $('#meal_to_add').val('1');
    } else if (dateInput.getHours() > 11 && dateInput.getHours() < 14) {
        $('#meal_to_add').val('2');
    } else if (dateInput.getHours() > 17 && dateInput.getHours() < 21) {
        $('#meal_to_add').val('3');
    } else {
        $('#meal_to_add').val('4');
    }

};


$('#time_eaten').on('change', updateMeal)