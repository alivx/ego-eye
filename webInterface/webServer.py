# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    webServer.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alivx <alivxlive@gmail.com>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/03/22 23:19:47 by alivx             #+#    #+#              #
#    Updated: 2020/03/22 23:38:52 by alivx            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


# Import flask
from flask import Flask, render_template, Response
import os
import sys
import inspect
sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))))
# Import redis visual data fetcher
from libs.redisStreamRetriever import *


app = Flask(__name__)
@app.route('/')
def video_feed():
    return Response(responseData(), mimetype='multipart/x-mixed-replace; boundary=frame')


app.run(host='0.0.0.0', port=8000)
