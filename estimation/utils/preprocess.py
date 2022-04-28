import time
import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm

from tf_pose import common
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path


def _process_video(video_path, e, height=1280, width=720):
    cap = cv2.VideoCapture(video_path)
    if cap.isOpened() is False:
        print("Error opening video stream or file")
    fps_time = 0

    frame_total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    for _ in tqdm(range(0, frame_total + 1)):
        ret_val, image = cap.read()
        dim = (height, width)
        if ret_val:
            # resize image
            image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
            humans = e.inference(image,
                                 resize_to_default=(width > 0 and height > 0),
                                 upsample_size=4.0)
            image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
            npimg = np.copy(image)
            image_h, image_w = npimg.shape[:2]
            centers = {}
            keypoints_list = []
            for human in humans:
                for i in range(common.CocoPart.Background.value):
                    if i not in human.body_parts.keys():
                        continue

                    body_part = human.body_parts[i]
                    x_axis = int(body_part.x * image_w + 0.5)
                    y_axis = int(body_part.y * image_h + 0.5)
                    center = [x_axis, y_axis]
                    centers[i] = center
                    keypoints_list.append(centers)

            cv2.putText(image, "FPS: %f" % (1.0 / (time.time() - fps_time)), (10, 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            # To display image
            cv2.imshow('Source', image)
            fps_time = time.time()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        else:
            break
    # print(keypoints_list)
    cap.release()
    cv2.destroyAllWindows()
    return keypoints_list


def process_video(video_path):
    width = 1280
    height = 720
    # resize_out_ratio = 4.0
    # show_process = False
    # tensorrt = False

    e = TfPoseEstimator(get_graph_path('cmu'), target_size=(width, height), trt_bool=False)

    keypoints_list = _process_video(video_path, e, width=width, height=height)
    features = [0] * 36
    keyp_list = []

    for i in range(0, len(keypoints_list)):
        k = -2
        for j in range(0, 18):
            k = k + 2
            # try:
            if k >= 36:
                break
            # print(k)
            # print(keypoints_list[i][j])
            features[k] = keypoints_list[i][j][0]
            features[k + 1] = keypoints_list[i][j][1]
            # except:
            #     features[k] = 0
            #     features[k + 1] = 0
        keyp_list.append(features)
    column_names = []
    for i in range(36):
        column_names.append(str(i))
    data = pd.DataFrame(keyp_list, columns=column_names)
    return data, keyp_list
