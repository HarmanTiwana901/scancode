from flask import Flask, render_template, Response
import cv2
from pyzbar.pyzbar import decode
import time

camera = cv2.VideoCapture(0)
app = Flask(__name__)

@app.route("/")
def main():
  return render_template ("index.html")

def gen_frames():  
    used_codes = []
    while True:
        success, frame = camera.read()  # read the camera frame
        for code in decode(frame):
            if code.data.decode('utf-8') not in used_codes:
                print('Approved!')
                print(code.data.decode('utf-8'))
                used_codes.append(code.data.decode('utf-8'))
                time.sleep(5)
            elif code.data.decode('utf-8') in used_codes:
                print('Sorry, this code has been alreadey used')
                time.sleep(5)
            else:
                pass
            print(code.type)
            print(code.data.decode('utf-8'))
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/capture')
def index():
    return render_template('cam.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
  
if __name__ == '__main__':
  app.run(debug=True)

