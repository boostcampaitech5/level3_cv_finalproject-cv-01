import pandas as pd
import os
import json
import argparse
from ingredient_list import allergy_list, all_ingredients

def extract_only_allergy(data_csv, out):
    data = pd.read_csv(data_csv)
    
    json_list = data['json_path']
    for json_path in json_list:
        label = json_path.split('/')[-2:-1]

        # make out dirs
        out_dir = os.path.join(out, label[0])
        os.makedirs(out_dir, exist_ok=True)
        
        # read json
        with open(json_path,'rt', encoding='utf-8-sig') as json_file:
            anno = json.load(json_file)

        #  "ingredients": [
        #   {
        #     "subtype": "meat",
        #     "ingredient": "chicken"
        #   }, ... 
        ingredient_list = anno['ingredients']
        new_list = []

        for ingredient in ingredient_list:
            name = ingredient['ingredient']

            # allergy it self
            if name in allergy_list.keys():
                if allergy_list[name] not in new_list:
                    new_list.append(allergy_list[name])

            # products that include allergies
            elif name in all_ingredients.keys():
                for allergy in all_ingredients[name]:
                    if allergy_list[allergy] not in new_list:
                        new_list.append(allergy_list[allergy])        

        anno['ingredients'] = new_list 

        # save json
        out_dir = os.path.join(out_dir, os.path.basename(json_path))
        with open(out_dir, 'w') as out_file:
            json.dump(anno, out_file, indent="\t")
        print(out_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default='./data/data_v1.csv')
    parser.add_argument('--out', type=str, default='./data/recipe_data_preprocessing/new_json')
    args = parser.parse_args()

    extract_only_allergy(args.data, args.out)
