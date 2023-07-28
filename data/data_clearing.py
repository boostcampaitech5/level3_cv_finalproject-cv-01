import pandas as pd
import os
import argparse


def data_clearing(target_file, delete_list_file, out_file):
    """ clear data and save as csv

    Args:
        target_file (str): data (csv)
        delete_list_file (str): list to delete from data (csv)
        out_file (str): output file path 
    """
    data = pd.read_csv(target_file)
    delete_list = pd.read_csv(delete_list_file)
    print("before :", len(data))

    # 제거 항목 추출
    delete_indices = delete_list[delete_list['제거/보류']=='제거']['id']
    
    # 제거
    data.drop(delete_indices, inplace=True)

    # 결과 저장
    data.to_csv(out_file, index=False)

    print("after :", len(data))

def file_clearing(base_dir, delete_list_file):
    """remove files in delete list

    Args:
        base_dir (str): data directory
        delete_list_file (str): list to delete from data (csv)
    """
    delete_list = pd.read_csv(delete_list_file)
    
    for idx, row in delete_list.iterrows():
        if row['제거/보류'] != '제거':
            continue

        try:
            img_path = os.path.join(base_dir, row['img_path'])
            os.remove(img_path)
            print("remove ", img_path)

            json_path = os.path.join(base_dir, row['json_path'])
            os.remove(json_path)
            print("remove ", json_path)
        except:
            pass

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--target', type=str, default='data/data.csv')
    parser.add_argument('--source', type=str, default='data_clearing.csv')
    parser.add_argument('--out', type=str, default='data/data_v1.csv')
    args = parser.parse_args()

    data_clearing(args.target, args.source, args.out)
    # file_clearing('data/recipe_data_preprocessing', 'data_clearing.csv')