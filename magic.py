def find_common_ingredients(ingredient_lists_list):
    """Takes in a list of ingredient lists and returns the ingredients 
    in common between (2+ occurences) lists within a dictionary"""

    all_ingredients = {}
    common_ingredients = []  # common_ingredients is a list so that we can sort

    for ingredient_list in ingredient_lists_list:
        for ingredient in ingredient_list:
            all_ingredients[ingredient] = all_ingredients.get(ingredient, 0) + 1

    for ingredient, count in all_ingredients.items():
        if count > 1:
            common_ingredients.append({'ingredient_id': ingredient.id,
                                       'ingredient': ingredient.name, 
                                       'count': count})

    common_ingredients = sorted(common_ingredients, 
                                key = lambda i: i['count'], # provide the value to sort by
                                reverse=True)


    return common_ingredients
    # returns a sorted list of dictionaries

def return_ingredient_list(ingredient_str):

    # replace all delimiters with commas
    pre_split = ingredient_str.replace('(', ',')
    pre_split = pre_split.replace('[', ',')
    pre_split = pre_split.replace('.', ',')
    pre_split = pre_split.replace(':', ',')

    # replace all special characters with blanks
    pre_split = pre_split.replace(')', '')
    pre_split = pre_split.replace(']', '')
    pre_split = pre_split.replace('*', '')

    # replace all adjectives with blanks
    pre_split = pre_split.replace('Organic', '')
    pre_split = pre_split.replace('Natural', '')

    # split the list on commas
    split_list = pre_split.split(',')

    ingredient_list = []
    
    for ingredient in split_list:
        ingredient = ingredient.lower().strip()
        if 'less than' in ingredient:
            break # exit loop so we don't add anything after this
        elif 'vitamins' in ingredient:
            break 
        elif 'ingredients' in ingredient:
            continue
        elif 'contains' in ingredient:
            continue
        elif ingredient == '':
            continue
        else:
            ingredient_list.append(ingredient)

    return ingredient_list 