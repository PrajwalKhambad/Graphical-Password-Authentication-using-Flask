from datetime import timedelta, datetime
import io
from flask import Flask, render_template, request
import base64
from io import BytesIO
import requests
import cv2
import firebase_admin
from firebase_admin import credentials, auth, storage
from PIL import Image
import numpy as np
import io
import base64

app = Flask(__name__)

# Initialize Firebase credentials
cred = credentials.Certificate('E:/EDI/Authentication_System/advanced-authentication-3ba33-firebase-adminsdk-basti-9d3f0d130d.json')
firebase_admin.initialize_app(cred,{
    'storageBucket' : 'advanced-authentication-3ba33.appspot.com'
})

@app.route('/')
def home():
    if(request.method=="POST_"):
        return render_template('display.html')
    return render_template('image_upload.html')

@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        # Get form data
        email = request.form['email']
        password = request.form['password']
        image = request.files['image']

        # Create new user in Firebase Authentication
        user = auth.create_user(email=email, password=password)

        # Upload image to Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(f'{user.uid}.jpg')
        blob.upload_from_string(image.read(), content_type='image/jpeg')
        image_url = blob.generate_signed_url(expiration=300)

        # Render the image_upload.html template with success message
        return render_template('image_upload.html', message=f'Successfully signed up! Image URL: {image_url}')

    # If request method is GET, render the image_upload.html template
    return render_template('image_upload.html')


@app.route('/display', methods=['GET', 'POST'])
def image():
    if request.method == 'POST':
        # Get email input from form
        global email
        email = request.form.get('email')

        # Get user info from Firebase Authentication
        global user
        try:
            user = auth.get_user_by_email(email)
        except:
            return "User not found", 404

        # Get image URL from Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(f'{user.uid}.jpg')
        expiration_time = timedelta(minutes=5)
        image_url = blob.generate_signed_url(expiration=datetime.utcnow() + expiration_time,
            method='GET')
        print(image_url)

        # Render HTML with image URL and email
        return render_template('display.html', image_url=image_url, email=email) 

    '''if request.method == 'POST':
        selectedOption = request.form.get('select')

        if selectedOption == '2*2':
            result = twoBy2()

        if selectedOption == '3*3':
            result = threeby3()   

    return render_template('display.html', result =result)''' 
    
    # If request method is GET, show form to input email
    return render_template('display.html')


@app.route('/half')
def my_fun():
    bucket = storage.bucket()
    blob = bucket.blob(f'{user.uid}.jpg')
    expiration_time = timedelta(minutes=5)
    image_url = blob.generate_signed_url(expiration=datetime.utcnow() + expiration_time)
    response =requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img = np.array(img)
    # img=cv2.imread("static/images/test.jpg")
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

@app.route('/user3')
def byuser():
    bucket = storage.bucket()
    blob = bucket.blob(f'{user.uid}.jpg')
    expiration_time = timedelta(minutes=5)
    image_url = blob.generate_signed_url(expiration=datetime.utcnow() + expiration_time)
    response =requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img = np.array(img)
    # img=cv2.imread("static/images/test.jpg")

    image = cv2.resize(img, (500,500))
    (height,width)=image.shape[:2]
    (cell_width,cell_height)=(width//2,height//2)

    '''width, height = img.size
    cell_width, cell_height = width // 3, height // 3
    cells = []'''

    # Divide the image into a 3x3 grid and encode each cell as base64
    cells = []
    for i in range(3):
        row = []
        for j in range(3):
            # Define bounding box for cell
            box = (j * cell_width, i * cell_height, (j + 1) * cell_width, (i + 1) * cell_height)
            cell = img.crop(box)

            # Encode cell as base64
            buffered = io.BytesIO()
            cell.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode('ascii')
            row.append(f"data:image/jpeg;base64,{img_str}")

        # Append row to grid
        cells.append(row)
    return render_template('index3.html', cells=cells)
    #return render_template('index3.html')


@app.route('/three', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # file = request.files['file']
        # img = Image.open(file)
        bucket = storage.bucket()
        blob = bucket.blob(f'{user.uid}.jpg')
        expiration_time = timedelta(minutes=5)
        image_url = blob.generate_signed_url(expiration=datetime.utcnow() + expiration_time)
        response =requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        width, height = img.size
        cell_width, cell_height = width // 3, height // 3
        cells = []

        # Divide the image into a 3x3 grid and encode each cell as base64
        cells = []
        for i in range(3):
            row = []
            for j in range(3):
                # Define bounding box for cell
                box = (j * cell_width, i * cell_height, (j + 1) * cell_width, (i + 1) * cell_height)
                cell = img.crop(box)

                # Encode cell as base64
                buffered = io.BytesIO()
                cell.save(buffered, format="JPEG")
                img_str = base64.b64encode(buffered.getvalue()).decode('ascii')
                row.append(f"data:image/jpeg;base64,{img_str}")

            # Append row to grid
            cells.append(row)
        return render_template('index3.html', cells=cells)
    return render_template('index3.html')


def twoBy2():
    bucket = storage.bucket()
    blob = bucket.blob(f'{user.uid}.jpg')
    expiration_time = timedelta(minutes=5)
    image_url = blob.generate_signed_url(expiration=datetime.utcnow() + expiration_time)
    response =requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img = np.array(img)
    # img=cv2.imread("static/images/test.jpg")
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
    return (encoded_imgs)


'''
@app.route('/third')
def threeby3():
    bucket = storage.bucket()
    blob = bucket.blob(f'{user.uid}.jpg')
    expiration_time = timedelta(minutes=5)
    image_url = blob.generate_signed_url(expiration=datetime.utcnow() + expiration_time)
    response =requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img = np.array(img)
    # img=cv2.imread("static/images/test.jpg")
    image = cv2.resize(img, (600,600))
    (h,w)=image.shape[:2]

    # divide the image into a 3x3 grid
    grid_h, grid_w = int(h/3), int(w/3)
    grid = [img[x:x+grid_h, y:y+grid_w] for x in range(0, h, grid_h) for y in range(0, w, grid_w)]
    # render the template with the divided image
    return render_template('result.html', grid=grid)
'''

# @app.route('/half')
# def my_fun():
#     bucket = storage.bucket()
#     blob = bucket.blob(f'{user.uid}.jpg')
#     expiration_time = timedelta(minutes=5)
#     image_url = blob.generate_signed_url(expiration=datetime.utcnow() + expiration_time)
#     response =requests.get(image_url)
#     img = Image.open(BytesIO(response.content))
#     img = np.array(img)
#     image = cv2.resize(img, (500,500))

#     # Divide the image into four equal parts
#     (h,w)=image.shape[:2]
#     (h_step, w_step)=(h//2, w//2)
#     parts=[image[:h_step, :w_step], 
#            image[:h_step, w_step:], 
#            image[h_step:, :w_step], 
#            image[h_step:, w_step:]]

#     encoded_imgs=[]
#     for part in parts:
#         _, data = cv2.imencode(".jpg", part)
#         encoded_part = base64.b64encode(data).decode('utf-8')
#         encoded_imgs.append(encoded_part)

#     return render_template("index2.html", encoded_imgs=encoded_imgs)

if __name__ == '__main__':
    app.run(debug=True)