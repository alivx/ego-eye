import cv2
import io
import numpy as np
import redis
from PIL import Image
# from flask import Flask, render_template, Response
import os
import sys
import inspect
sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))))
from libs import redisConnection as redisConnection


#Make connection to redis
rcon = redisConnection("localhost")
#Start a pipeline for MULTI/EXEC
p = rcon.pipeline()

def get_last():
    """
    get_last get latest vData from redis stream

    Returns:
        bytes: visual data
    """
    vData = p.xrevrange("local_cam", count=1).execute()
    last_id = vData[0][0][0]
    data = io.BytesIO(vData[0][0][1].get(b'image'))
    img = Image.open(data)
    arr = np.array(img)
    ret, img = cv2.imencode('.jpg', arr)
    print("{0}\t{1}".format(ret, last_id))
    return img.tobytes()


def responseData():
    """
    responseData continues return visual data
    Yields:
        last visual data return
    """
    while True:
        yield (b'--frame\r\n\tContent-Type: image/jpeg\r\n\r\n' + get_last() + b'\r\n\r\n')