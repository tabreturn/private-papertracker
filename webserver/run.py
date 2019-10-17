from cv.DetectTiles import DetectTiles
from flask import Flask, jsonify, render_template, request
import base64
import cv2
import cv2.aruco as aruco
import numpy as np

app = Flask(__name__)
app.config['UPLOADS'] = 'static/tmp'

@app.route('/')
def papertracker():
    return render_template('papertracker.html')

@app.route('/snap', methods=['PUT'])
def snap():
    # convert base64 string to binary image
    b64string = request.values['imageBase64'].split(',')[1]
    b64image = np.fromstring(base64.b64decode(b64string), np.uint8)
    # save image
    sessionid = request.values['sessionid']
    count = request.values['count']
    filename = ('{}/{}-{}.png').format(app.config['UPLOADS'], sessionid, count)
    snap = cv2.imdecode(b64image, cv2.IMREAD_COLOR)
    cv2.imwrite(filename, snap)

    if int(count) == 2:
        # detect tiles after two photos snapped
        coords1 = DetectTiles('test', 'cv/marker_test/') # uncomment for test image
        #coords1 = DetectTiles(sessionid+'-1', 'static/tmp/')
        #coords2 = DetectTiles(sessionid+'-2', 'static/tmp/')

        print( coords1.arucoDetect() )

        return jsonify(coords1.arucoDetect())

    return jsonify('2 images required')

if __name__ == '__main__':
    app.run()
