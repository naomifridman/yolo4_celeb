import json
from pathlib import Path
from argparse import ArgumentParser

import numpy as np
import cv2
import os


# input image width/height of the yolov4 model, set by command-line argument
img_size  = 416

# Minimum width/height of objects for detection (don't learn from
# objects smaller than these
min_size = 5

def calc_box(x, y, w, h, img_w, img_h):
    x = max(int(x), 0)
    y = max(int(y), 0)
    w = min(int(w), img_w - x)
    h = min(int(h), img_h - y)
    w_rescaled = float(w) * img_size  / img_w
    h_rescaled = float(h) * img_size / img_h
    if w_rescaled < min_size or h_rescaled < min_size:
        return -999,0,0,0
    else:
        cx = (x + w / 2.) / img_w
        cy = (y + h / 2.) / img_h
        nw = float(w) / img_w
        nh = float(h) / img_h
        return cx, cy, nw, nh
        
     
def txt_line(cls, x, y, w, h, img_w, img_h):
    """Generate 1 line in the txt file."""
   
    cx, cy, nw, nh = calc_box(x, y, w, h, img_w, img_h)
    if (cx < -900):
        return ''
    return '%d %.6f %.6f %.6f %.6f\n' % (cls, cx, cy, nw, nh )

"""
rm_txts(output_dir)
    process('test', 'raw/annotation_val.odgt', output_dir)
    process('train', 'raw/annotation_train.odgt', output_dir)
    print('creating ', 'crowdhuman-%s.data' % args.dim)
"""
def process_crowdhuman(set_='test', annotation_filename='raw/annotation_val.odgt',
            output_dir=None):
    """Process either 'train' or 'test' set."""
    assert output_dir is not None
    output_dir.mkdir(exist_ok=True)
    jpgs = []
    with open(annotation_filename, 'r') as fanno:
        for raw_anno in fanno.readlines():
            anno = json.loads(raw_anno)
            ID = anno['ID']  # e.g. '273271,c9db000d5146c15'
            
            jpg_path = output_dir / ('%s.jpg' % ID)
            if not os.path.isfile(jpg_path): 
               print(jpg_path, ' not found ')
               continue
               
            print('Processing ID: %s' % ID)
            img_h, img_w, img_c = image_shape(ID, output_dir)
            assert img_c == 3  # should be a BGR image
            txt_path = output_dir / ('%s.txt' % ID)
            # write a txt for each image
            with open(txt_path.as_posix(), 'w') as ftxt:
                for obj in anno['gtboxes']:
                    if obj['tag'] != 'person':
                        continue  # ignore non-human
                    """
                    if 'hbox' in obj.keys():  # head
                        line = txt_line(0, obj['hbox'], img_w, img_h)
                        if line:
                            ftxt.write(line)
                    """
                    if 'fbox' in obj.keys():  # full body
                        line = txt_line(1, obj['fbox'], img_w, img_h)
                        if line:
                            ftxt.write(line)
             # full path is needed
            jpgs.append(jpg_path)
    # write the 'data/crowdhuman/train.txt' or 'data/crowdhuman/test.txt'
    set_path = output_dir / ('%s.txt' % set_)
    with open(set_path.as_posix(), 'w') as fset:
        for jpg in jpgs:
            fset.write('%s\n' % jpg)


def rm_txts(output_dir):
    """Remove txt files in output_dir."""
    for txt in output_dir.glob('*.txt'):
        if txt.is_file():
            txt.unlink()


            
