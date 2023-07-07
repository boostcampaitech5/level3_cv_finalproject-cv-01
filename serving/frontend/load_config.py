from dataset import database
import json

class Config:
    def __init__(self):
        with open('./config.json','r') as f:
            self.config = json.load(f)
        self.checklist = self.config['checklist']
        self.ingredients_dict = self.config['ingredients_dict']
        self.class_dict = self.config['class_dict']
        self.IP = self.config['IP']
        self.PORT = self.config["PORT"]
        self.ADDR = (self.IP, self.PORT)

    def set_checklist(self,checklist):
        self.config['checklist'] = checklist

    def save_checklist(self):
        with open('./config.json','w') as f:
            json.dump(self.config,f,indent=4)

config = Config()


if __name__ == '__main__':
    db_keys = database.keys()
    db_values = database.values()
    db_v_set = set([])
    for values in db_values:
        db_v_set = db_v_set.union(set(values))

    user_checklist = {v:False for v in db_v_set}
    ingredients_dict = {v:v for v in db_v_set}
    class_dict = {v:v for v in db_keys}
    print(user_checklist)
    print(ingredients_dict)
    print(class_dict)
    config = {'checklist':user_checklist,
            'ingredients_dict':ingredients_dict,
            'class_dict':class_dict}


    with open('./config,json','w') as f:
        json.dump(config,f,indent=4)