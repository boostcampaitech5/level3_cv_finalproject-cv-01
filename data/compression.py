import os
import argparse
from PIL import Image 

def main(base_dir):
    """compress dataset by resizing to 512 and saving as jpg

    Args:
        base_dir (str): base path where data locates
    """

    print("Compressing...")
    labels = os.listdir(base_dir)

    for label in labels:    
    # for i in range(40, len(labels)):
    #     label = labels[i]
        img_dir = os.path.join(base_dir, label + '/png')
        if not os.path.exists(img_dir):
            continue 

        # create save dir
        save_dir = os.path.join(base_dir, label + '/jpg')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        img_list = os.listdir(img_dir)
        for img_name in img_list:
            # skip file name starts with . (ex. '._name.png')
            if img_name[0] == '.' or img_name[-4:] != '.png':
                continue
            
            img = Image.open(os.path.join(img_dir, img_name))

            # resize
            img = img.resize((512, 512))

            # save as jpg
            img = img.convert("RGB") # convert mode from RGBA to RGB
            save_name = img_name.split('.')[0] + '.jpg'
            img.save(os.path.join(save_dir, save_name))
            print("Image saved in " + os.path.join(save_dir, save_name))
    
    print("Compression Done!")

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', type=str, default='./Computer Vision Lab')
    args = parser.parse_args()

    main(args.base_dir)