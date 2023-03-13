from flask import Flask, render_template, request , jsonify , flash
from PIL import Image
import base64
import io
import cv2


app = Flask(__name__)
'''
@app.route('/image_upload' , methods=['GET' , 'POST'])
def image_split(img):
    if request.method=='POST':
        img=request.files['file']
    img=cv2.imread("static/test.jpg")
    image=cv2.resize(img,(300,300))
    h,w=image.shape[:2]

    p1=w//3
    p2=2*w//3

    p3=h//3
    p4=2*h//3

    img1=image[0:p1,0:p3]
    img2=image[p1:p2,0:p3]
    img3=image[p2:w,0:p3]

    img4=image[0:p1,p3:p4]
    img5=image[p1:p2,p3:p4]
    img6=image[p2:w,p3:p4]

    img7=image[0:p1,p4:h]
    img8=image[p1:p2,p4:h]
    img9=image[p2:w,p4:h]
'''


@app.route('/')
def hello_world():
    # Full Script.
    img = Image.open('static/images/test.jpg')
    data = io.BytesIO()
    img.save(data, "JPEG")
    encoded_img_data = base64.b64encode(data.getvalue())

    return render_template("index.html", img_data=encoded_img_data.decode('utf-8'))

@app.route('/half')
def my_fun():
    img=cv2.imread("static/test.jpg")
    image = cv2.resize(img, (500,500))
    (h,w)=image.shape[:2]
    (cX,cY)=(w//2,h//2)

    topLeft = image[0:cY, 0:cX]
    topRight = image[0:cY, cX:w]
    bottomLeft = image[cY:h, 0:cX]                                                                                                  
    bottomRight = image[cY:h, cX:w]

    _ , data1=cv2.imencode(".jpg",topLeft)
    _ , data2=cv2.imencode(".jpg",topRight)
    _ , data3=cv2.imencode(".jpg",bottomLeft)
    _ , data4=cv2.imencode(".jpg",bottomRight)

    enc1=base64.b64encode(io.BytesIO(data1).getvalue()).decode('utf-8')
    enc2=base64.b64encode(io.BytesIO(data2).getvalue()).decode('utf-8')
    enc3=base64.b64encode(io.BytesIO(data3).getvalue()).decode('utf-8')
    enc4=base64.b64encode(io.BytesIO(data4).getvalue()).decode('utf-8')

    encoded_imgs=[enc1,enc2,enc3,enc4]

    # print(enc1)
    print(type(enc1))

    return render_template("index2.html", encoded_imgs=encoded_imgs)

@app.route('/upload' , methods=['GET',"POST"])
def upload():
    return render_template("image_upload.html")

def show_uploaded():
    if request.method=='POST':
        img=request.files['file']
    image=cv2.resize(img,(300,300))

    _, data1=cv2.imencode(".jpg",image)
    encoded = base64.b64encode(io.BytesIO(data1).getvalue()).decode('utf-8')
    return render_template("image_upload.html", encoded = encoded)


if __name__ == '__main__':
    app.run(debug=True)