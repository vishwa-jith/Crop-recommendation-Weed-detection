import pickle
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import tensorflow as tf
import os
from tqdm import tqdm
import json
import warnings
import pickle
import base64
from PIL import Image
from io import BytesIO
warnings.filterwarnings('ignore')


def loadpickles(filename):
    with open(filename, 'rb') as f:
        model = pickle.load(f)
    return model


def getSeason():
    month = time.strftime("%m")
    seasons = {'Kharif     ': ['7', '8', '9', '10'],
               'Autumn     ': ['9', '10', '11'],
               'Summer     ': ['3', '4', '5', '6'],
               'Winter     ': ['12', '1', '2'],
               'Rabi       ': ['10', '11', '12', '1', '2', '3']}
    season = ""
    for key, value in seasons.items():
        for val in value:
            if(val == str(int(month))):
                season = key
                break
    return season


def iou_calc(bb1, bb2):

    true_xmin, true_ymin, true_width, true_height = bb1
    bb_xmin, bb_ymin,  bb_width, bb_height = bb2

    true_xmax = true_xmin + true_width
    true_ymax = true_ymin + true_height
    bb_xmax = bb_xmin + bb_width
    bb_ymax = bb_ymin + bb_height

    # calculating area
    true_area = true_width * true_height
    bb_area = bb_width * bb_height

    # calculating itersection cordinates
    inter_xmin = max(true_xmin, bb_xmin)
    inter_ymin = max(true_ymin, bb_ymin)
    inter_xmax = min(true_xmax, bb_xmax)
    inter_ymax = min(true_ymax, bb_ymax)

    if inter_xmax <= inter_xmin or inter_ymax <= inter_ymin:
        iou = 0

    else:
        inter_area = (inter_xmax - inter_xmin) * (inter_ymax - inter_ymin)

        iou = inter_area / (true_area + bb_area - inter_area)

    assert iou <= 1
    assert iou >= 0

    return iou


def readb64(base64_string):
    sbuf = BytesIO()
    sbuf.write(base64.b64decode(base64_string))
    pimg = Image.open(sbuf)
    return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)


def detection(img_path, confidence=0.9, iou_thresh=0.1):

    model_path = './notebooks/weed Detection/Models/RCNN_crop_weed_classification_model1.h5'
    svm_model_path = './notebooks/weed Detection/Models/svm_classifier.pkl'
    model = tf.keras.models.load_model(model_path)
    model_without_last_two_fc = tf.keras.models.Model(
        model.inputs, model.layers[-5].output)
    svm_model = loadpickles(svm_model_path)

    # appling selective search
    img = readb64(img_path)
    # img = plt.imread(img_path)
    cv2.setUseOptimized(True)
    ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()
    ss.setBaseImage(img)
    ss.switchToSelectiveSearchFast()
    rects = ss.process()
    sel_rects = rects[:50]

    pred_crop = []
    pred_weed = []
    for index, rect in tqdm(enumerate(sel_rects)):

        x, y, w, h = rect
        roi = img[y:y+h, x:x+w, :]
        resized_roi = cv2.resize(roi, (224, 224))/255

        # Feature extraction

        feature = model_without_last_two_fc.predict(
            resized_roi.reshape(-1, 224, 224, 3))

        # SVM prediction
        pred = svm_model.predict_proba(feature.reshape(-1, 4096))
        pred_lab = svm_model.predict(feature.reshape(-1, 4096))

        if pred_lab == 'crop' and np.max(pred) > confidence:
            pred_crop.append([list(rect), np.max(pred)])
        elif pred_lab == 'weed' and np.max(pred) > confidence:
            pred_weed.append([list(rect), np.max(pred)])

    final = []

    # Detection for crop class
    if len(pred_crop) != 0:
        pred_score_crop = [x[1] for x in pred_crop]
        pred_bb_crop = [x[0] for x in pred_crop]

        for i in range(len(pred_crop)):
            temp_bb, temp_score = pred_bb_crop.copy(), pred_score_crop.copy()
            if len(temp_bb) != 0:

                max_score_box = temp_bb[np.argmax(temp_score)]

                if [max_score_box, np.max(temp_score)] not in final:
                    final.append([max_score_box, np.max(temp_score), 'crop'])
                    index_should_del = []

                    for ind, other_bb in enumerate(temp_bb):
                        iou_score = iou_calc(max_score_box, other_bb)

                        # Non maximum suppression(nms)

                        if iou_score >= iou_thresh:
                            index_should_del.append(ind)

                    pred_bb_crop = []
                    pred_score_crop = []
                    for bb_index, bb_value in enumerate(temp_bb):
                        if bb_index not in index_should_del:
                            pred_bb_crop.append(bb_value)

                    for score_index, score_value in enumerate(temp_score):
                        if score_index not in index_should_del:
                            pred_score_crop.append(score_value)
                else:
                    continue

            else:
                break

    # Detection for weed class

    if len(pred_weed) != 0:
        pred_score_weed = [x[1] for x in pred_weed]
        pred_bb_weed = [x[0] for x in pred_weed]

        for i in range(len(pred_weed)):
            temp_bb, temp_score = pred_bb_weed.copy(), pred_score_weed.copy()
            if len(temp_bb) != 0:

                max_score_box = temp_bb[np.argmax(temp_score)]

                if [max_score_box, np.max(temp_score)] not in final:
                    final.append([max_score_box, np.max(temp_score), 'weed'])
                    index_should_del = []

                    for ind, other_bb in enumerate(temp_bb):
                        iou_score = iou_calc(max_score_box, other_bb)

                        if iou_score >= iou_thresh:
                            index_should_del.append(ind)

                    pred_bb_weed = []
                    pred_score_weed = []
                    for bb_index, bb_value in enumerate(temp_bb):
                        if bb_index not in index_should_del:
                            pred_bb_weed.append(bb_value)

                    for score_index, score_value in enumerate(temp_score):
                        if score_index not in index_should_del:
                            pred_score_weed.append(score_value)
                else:
                    continue

            else:
                break

    imOut = img.copy()
    for rect, score, cls in final:

        x, y, w, h = rect
        if cls == 'weed':
            color = (255, 0, 0)
        if cls == 'crop':
            color = (0, 255, 0)

        cv2.rectangle(imOut, (x, y), (x+w, y+h), color, 2)

        cv2.putText(imOut, cls+':'+str(round(score*100, 2)), (x, y-8),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
    plt.imshow(imOut)
    im_bytes = imOut.tobytes()
    im_b64 = base64.b64encode(im_bytes)
    # cv2.imwrite('prediction.jpeg', imOut)

    return final


def convertToList(output):
    output[0] = list(map(int, output[0]))
    output[1] = float(output[1])
    output[2] = str(output[2])
    return output
