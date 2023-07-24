import os
import pandas as pd
import argparse

def to_csv(base_dir, save_dir):
    label_list = os.listdir(base_dir + '/image')

    id = 0
    ids = []
    class_ids = []
    labels = []
    img_paths = []
    json_paths = []

    for label in label_list:
        img_dir = os.path.join(base_dir + '/image', label)
        json_dir = os.path.join(base_dir + '/json', label)

        img_list = os.listdir(img_dir)  
        json_list = os.listdir(json_dir)

        for img in img_list:
            class_id = img.split('.')[0].split('_')[-1]

            for json in json_list:
                if json[0]=='.' or json.split('.')[-1] != 'json':
                    continue 

                if int(json.split('_')[0]) == int(class_id):
                    ids.append(id)
                    id += 1
                    class_ids.append(class_id)
                    labels.append(label)

                    img_path = os.path.join(img_dir, img)
                    json_path = os.path.join(json_dir, json)\
                    
                    # window '\' -> '/'
                    img_path = img_path.replace("\\", "/")
                    json_path = json_path.replace("\\", "/")
                    print(img_path)
                    print(json_path)

                    img_paths.append(img_path)
                    json_paths.append(json_path)

    print(len(ids))
    print(len(class_ids))
    print(len(labels))
    print(len(img_paths))
    print(len(json_paths))

    df = pd.DataFrame({"id" : ids,
                       "class_id" : class_ids,
                       "label" : labels,
                       "img_path" : img_paths,
                       "json_path" : json_paths})
    df.to_csv(save_dir, index=False)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', type=str, default= './data')
    parser.add_argument('--out_dir', type=str, default='./data/data.csv')
    args = parser.parse_args()

    to_csv(args.base_dir, args.out_dir)     
    