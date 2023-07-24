import numpy as np
import json
import server
from load_config import config

ingredients_dict, class_dict = config.ingredients_dict , config.class_dict

def match_ingredient(user_list, ingredients):
    user_list = set(user_list)
    ingredients = set(ingredients)
    union_recipe = user_list & ingredients
    return list(union_recipe)

def server_result_parsing(server_data):
    json_data = json.loads(server_data)[0]
    class_name = json_data['class']
    ingredients = json_data['recipe']
    
    return class_name, ingredients 

def client_process(ADDR,img_data,user_data):
    server_data = server.connect_with_server(ADDR,img_data) 
    class_name , ingredients = server_result_parsing(server_data)
    warning_ingredient = match_ingredient(user_data,ingredients)
    repr = result_repr(class_name, ingredients, warning_ingredient)
    return repr

def result_repr(class_name, ingredients,warning_ingredients):
    class_repr = f'탐지된 음식 : {class_dict[class_name]}'
    recipe_repr = f'음식 재료 : {", ".join([ingredients_dict[i] for i in ingredients])}'
    warning_repr = f'사용자 위험 재료 : {", ".join([ingredients_dict[i] for i in warning_ingredients])}'
    repr = [class_repr,recipe_repr,warning_repr]
    return repr

if __name__ == '__main__':
    import server
    import cv2
    client_process(cv2.imread('./sample_img.jpg',cv2.IMREAD_COLOR),None)