import os
import shutil
import argparse
import json
import pandas as pd
import natsort

from PIL import Image 
from data import database
from generate_csv import to_csv
from ingredient_list import allergy_list

def main(new_data_dir, base_dir, csv_out):
    # create json and copy img
    create_new_data(new_data_dir, base_dir)

    # create new csv
    to_csv(base_dir, csv_out)
    

def create_new_data(new_dir, base_dir):    
    label_list = os.listdir(new_dir)

    for label in label_list:
        new_img_dir = os.path.join(new_dir, label)
        json_dir = os.path.join(os.path.join(base_dir, 'json'), label)
        img_dir = os.path.join(os.path.join(base_dir, 'image'), label)

        # get list of json
        json_list = natsort.natsorted(os.listdir(json_dir))

        # get latest instance number and country from json
        latest_json = os.path.join(json_dir, json_list[-1])
        with open(latest_json, 'rt', encoding='utf-8-sig') as json_file:
            json_data = json.load(json_file)
        latest_num = json_data['instance_num'] + 1
        country = json_data['country']

        # get ingredients from database
        ingredients = []

        basic_ingredients = database.database[label]
        for ingd in basic_ingredients:
            ingredients.append(allergy_list[ingd])

        out_json = {"instance_num": latest_num,
                    "country": country,
                    "food_class": label,
                    "ingredients": ingredients}

        img_list = os.listdir(new_img_dir)
        for img_path in img_list:
            # create json file        
            out_path = f"{latest_num}_{country}_{label}.json"
            out_path = os.path.join(json_dir, out_path)
            with open(out_path, 'w') as out_file:
                json.dump(out_json, out_file, indent="\t")
            
            # resize image
            img = Image.open(os.path.join(new_img_dir, img_path))
            
            img = img.resize((244, 244))
            img = img.convert("RGB")

            # save image
            out_img = f"{label}_{latest_num}.jpg"
            img.save(os.path.join(img_dir, out_img))

            latest_num += 1

            print("json saved at :",out_path)
            print("img copied to :",os.path.join(img_dir, out_img))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', type=str, default= './data')
    parser.add_argument('--new_data_dir', type=str, default= './data/new_data')
    parser.add_argument('--csv_out', type=str, default= './data/data_v4.csv')
    args = parser.parse_args()

    main(args.new_data_dir, args.base_dir, args.csv_out)     