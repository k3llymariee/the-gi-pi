"use strict";

const getFoodData = () => {
    // Get the up to date food data from DB for the signed in user

    $.get('/user_foods.json', insertFoodData);
}

const insertFoodData = (res) => {
    // Once the data has been provided by the server,
    // insert it into the page as an HTML string.

    const listOfFoods = res.foods;
    const container = $('#display-db-search');
    container.empty();
    container.append('<ul>')

    for (const currentFood of listOfFoods) {

        // consider adding each food as an option and allow them to add with timestamp to food log here
        container.append(`
            <li>
                   ${currentFood.name} (${currentFood.brand}) 
                   <a href="/add_food/${currentFood.id}">+</a>
            </li>`
        );
    }

    container.append('</ul>')
}



$('#search-food').on('submit', (evt) => {
    evt.preventDefault();

    const searchTerm = $('#search_term').val();

    $.get(`/food_search/${searchTerm}`, (res) => {
        
        const foods = res["foods"]
        const container = $('#display-search');
        container.empty()
        container.append(`<br><p>
                            Can't find what you're looking for? 
                            <a href='/manual_add'>Add it manually</a>
                        </p>`)

        for (const food of foods) {
            container.append(`
                <div class='food'>
                    <p>Brand: ${food.brand_name}</p>
                    <p>Name: ${food.brand_name_item_name}</p>
                    <img src='${food.photo.thumb}' /><br>
                    <p>NIX ID: ${food.nix_item_id}</p>
                </div>`
            );
        };
    });
  });

$('#db-search').on('submit', (evt) => {
    evt.preventDefault();

    const dbSearchTerm = $('#db_search_term').val();

    $.get(`/db_food_search/${dbSearchTerm}`, (res) => {
        
        const foods = res["foods"]
        const container = $('#display-db-search');
        container.empty()

        if (foods.length === 0) {
            container.append('<br><i>No foods found</i>');
        }

        else {

            container.append("<ul>");

            for (const food of foods) {
                container.append(`<div>
                    <p>Foods from demo database search:</p>
                    <li>${food.food} (${food.brand})
                    <a href='/add_food/${food.id}'>ADD ME</a></li>
                    </li></div>`
                );

            container.append('</ul');
            };
        }
    });
});

// Get intial foods when page initially loads!
getFoodData();