import numpy as np



def match_recipe(user_list, recipe):
    user_list = set(user_list)
    recipe = set(recipe)
    union_recipe = user_list & recipe
    return union_recipe

