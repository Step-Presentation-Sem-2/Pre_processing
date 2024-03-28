import numpy as np
from tensorflow.keras import backend as kb
from PIL import Image
import config as cg
import os

def preprocess_input(image_np, data_format): 
    x_temp = np.copy(image_np)
    if data_format is None:
        data_format = kb.image_data_format()
    assert data_format in {'channels_last', 'channels_first'}
    if data_format == 'channels_first':
        x_temp = x_temp[:, ::-1, ...]
        x_temp[:, 0, :, :] -= cg.mean[0]
        x_temp[:, 1, :, :] -= cg.mean[1]
        x_temp[:, 2, :, :] -= cg.mean[2]
    else:
        x_temp = x_temp[..., ::-1]
        x_temp[..., 0] -= cg.mean[0]
        x_temp[..., 1] -= cg.mean[1]
        x_temp[..., 2] -= cg.mean[2]

    return x_temp
