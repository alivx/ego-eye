# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    visualDataStreamer.py                              :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alivx <alivxlive@gmail.com>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/03/20 13:25:58 by alivx             #+#    #+#              #
#    Updated: 2020/03/24 23:21:02 by alivx            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# Load modules
import cv2
import sys
import os
import sys
import inspect
sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))))
from libs import redisConnection as redisConnection


class VisualInput():
    """
    VisualInput retvices frames from the visual source video file/ Camera URL/Webcam

    Returns:
        step: frame order
        frame: image

    """

    def __init__(self, vType=0, fps=15.0):
        self.cam = cv2.VideoCapture(vType)
        self.cam.set(cv2.CAP_PROP_FPS, fps)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def __iter__(self):
        self.step = -1
        return self

    def __next__(self):
        self.step += 1
        try:
            ret_val, img0 = self.cam.read()
        except:
            print("Error reading visual data..")
        img = img0
        return self.step, img


def startStream(redisHost="localhost", visualSourceName="local_cam"):
    """
    startStream streaming the frames into redis stream

    Args:
        redisHost (str, optional): Redis Hostname URL/IP. Defaults to "localhost".
        visualSourceName (str, optional): visual data source name. Defaults to "local_webcam".
    """

    # Load redis connection obj
    rcon = redisConnection(redisHost)
    # Load the visualInput vType=0 for webcam
    framesStream = VisualInput(vType=0, fps=15)
    # Move though the frames
    for (orderID, img) in framesStream:
        # reading frames
        status, frame = cv2.imencode(".jpg", img)
        # Compose them into message
        message = {'orderID': orderID, 'image': frame.tobytes()}
        # Stream the frames into redis stream
        streamID = rcon.xadd(visualSourceName, message,maxlen=10)
        print("Setting vdata with ID: {0}, Order: {1}, Image: {2}".format(
            streamID, message['orderID'], message['image'][0:10]))


startStream()
