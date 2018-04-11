from __future__ import print_function
import sys
from glob import glob

import pandas as pd
from PIL import Image
from keras.models import load_model
import numpy as np
from keras import backend as K



# FOR LOADING IMAGES AND LABELS


def dir_to_dataset(glob_files, loc_train_labels=""):
    print('\n')
    print("Gonna process:\t %s"%glob_files)
    dataset = []
    for file_count, file_name in enumerate(sorted(glob(glob_files))):
        if file_count % 100 == 0:
            sys.stdout.write(".")
            sys.stdout.flush()
        img = Image.open(file_name).convert('LA') #tograyscale
        pixels = [f[0] for f in list(img.getdata())]
        #print( file_name)
        dataset.append(pixels)

    print("\n TrainLabels ..")
    if len(loc_train_labels) > 0:
        df = pd.read_csv(loc_train_labels)
        print("\t Labels loaded  ..")
        return np.array(dataset), np.array(df["Class"])
    else:
        return np.array(dataset)

x = dir_to_dataset('./evaul_data/*.png')
img_rows, img_cols = 28, 28

if K.image_dim_ordering() == 'th':
    x = x.reshape(x.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
else:
    x = x.reshape(x.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)

x = x.astype('float32')
x /= 255


model = load_model('./OCR_cnn.h5')
output_labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Z', 'S']
res = model.predict(x, verbose=1)
print("\n")
for r in res:

    print(output_labels[np.argmax(r)])
