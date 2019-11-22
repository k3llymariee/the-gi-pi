"use strict";

const updateMeal = () => {

    const dateInput = new Date($('#time_eaten').val());

    // if timeEaten is between 6am and 9am -> value of meal = breakfast
    // if timeEaten is between 11:00am and 1:30 pm -> valeu of meal = lunch
    // if timeEaten is between 5:30pm and 9:00pm -> value of meal = dinner
    // ELSE value of meal = snack

    if (dateInput.getHours() > 6 && dateInput.getHours() < 9) {
        $('#meal_to_add').val('1');  // breakfast
    } else if (dateInput.getHours() > 11 && dateInput.getHours() < 14) {
        $('#meal_to_add').val('2');  // lunch
    } else if (dateInput.getHours() > 17 && dateInput.getHours() < 21) {
        $('#meal_to_add').val('3'); // dinner
    } else {
        $('#meal_to_add').val('4');  // snacks
    }
};

const pad = (n) => {
    if (n < 10) {
        return '0' + n
    } else {
        return n
    }
};

const defaultTime = () => {

    const currentDate = new Date()
    const date = currentDate.getDate();
    const month = currentDate.getMonth() + 1;  //January is 0 not 1
    const year = currentDate.getFullYear();
    const hours = currentDate.getHours();
    const minutes = currentDate.getMinutes();

    // The format is "yyyy-MM-ddThh:mm"

    const currentDateTime  = pad(year) + "-" + pad(month) + "-" + pad(date)
        + "T" + pad(hours) + ":" + pad(minutes);

    $('#time_eaten').val(currentDateTime)

    updateMeal();
}

defaultTime();

$('#time_eaten').on('change', updateMeal)