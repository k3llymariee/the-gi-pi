def find_common_ingredients(ingredient_lists_list):
    """Takes in a list of ingredient lists and returns the ingredients 
    in common between (2+ occurences) lists within a dictionary"""

    all_ingredients = {}
    common_ingredients = {}

    for ingredient_list in ingredient_lists_list:
        for ingredient in ingredient_list:
            all_ingredients[ingredient] = all_ingredients.get(ingredient, 0) + 1

    for ingredient, count in all_ingredients.items():
        if count > 1:
            common_ingredients[ingredient] = count

    return common_ingredients