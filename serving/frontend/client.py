import os
import pickle
import sys
import PyQt5
from PyQt5.QtWidgets import *




def main(config):
    checklist_path = config['checklist_path']
    if not os.path.exists(checklist_path):
        checklist = {'test':False}
    else:
        with open(checklist_path,'rb') as f:
            checklist = pickle.load(f)
    print(sys.argv)
    app = QApplication(sys.argv)
    window = QWidget()
    window.show()
    app.exec_()
    print(app)

    






if __name__ == '__main__':
    config = {}
    config['classes']={'test':False}
    config['checklist_path']='./user_checklist.pickle'
    main(config)