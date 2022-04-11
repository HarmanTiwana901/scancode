from flask import Flask, render_template, Response, redirect, flash, url_for, current_app
import cv2
from matplotlib.pyplot import bar
from numpy import prod
from pyzbar.pyzbar import decode
import time
import requests
import json
import pprint
import urllib.request


camera = cv2.VideoCapture(0)
app = Flask(__name__)

@app.route("/")
def main():
  return render_template ("index.html")

product_data = []

# Barcode code 
def gen_frames():  

    used_codes = []
    while True:
        success, frame = camera.read()  # read the camera frame
        for code in decode(frame):
            if code.data.decode('utf-8') not in used_codes:
                print('Approved!')
                print(code.data.decode('utf-8'))
                print("Our results")
                product_data.append(details(code.data.decode('utf-8')))
                storeData()
                break
            else:
                pass

        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/details')
def storeData():
    print("Current values of product_data: ")
    print(product_data)
    return render_template('details.html', data=product_data)
    

@app.route('/capture')
def index():
    return render_template('cam.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def details(barcode):
    url = "https://api.barcodelookup.com/v3/products?barcode="+barcode+"&formatted=y&key=gpt1sdbzwlplq8ymwu35o9ehscvwer"
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())
    barcode = data["products"][0]["barcode_number"]
    print ("Barcode Number: ", barcode, "\n")

    name = data["products"][0]["title"]
    print ("Title: ", name, "\n")

    print ("Entire Response:")
    pprint.pprint(data)
    return data
  
if __name__ == '__main__':
  app.run(debug=True)

