from datetime import datetime
import json
import io
import sqlite3

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt, image

# from detect import run



def start_detect(base, path):
    run(weights=base, save_crop=True, source=path, nosave=True)


def add_row(res, text, img=None, crop=None):
    date = datetime.now()
    res = json.dumps({'result': res})
    # text = 'Hello'
    
    conn = sqlite3.connect('base.db')
    cur = conn.cursor()
    cur.execute(f'''
        insert into base
            values (?, ?, ?, ?, ?)
    ''', (date, text, crop, img, res))
    conn.commit()
    print('Добавлено в базу')
    cur.close()
    conn.close()


def create_table():
    conn = sqlite3.connect('base.db')
    cur = conn.cursor()
    with open('create.sql') as f:
        text = f.read()
        
    cur.executescript(text)
    conn.commit()
    print('Create')
    cur.close()
    conn.close()
    

def read_all():
    conn = sqlite3.connect('base.db')
    cur = conn.cursor()
    cur.execute('select * from base;')
    n = 1
    for it in cur.fetchall():
        img = image.imread(f'images/crops/{it[2]}')
        plt.imshow(img)
        plt.title(it[1])
        plt.axis('off')
        plt.show()
        img = image.imread(f'images/images/{it[3]}')
        plt.imshow(img)
        plt.title(it[1])
        plt.axis('off')
        plt.show()        
    print('Read')
    cur.close()
    conn.close()

if __name__ == '__main__':
   read_all()
 
