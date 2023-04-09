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
import random

app = Flask(__name__)

# Initialize Firebase credentials
cred = credentials.Certificate('D:/AI-B[Sem 4]/EDI_Sem4/advanced-authentication-3ba33-firebase-adminsdk-basti-91ee0a3617.json')
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
        # global email
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
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
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

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form['email']

        # retrieve images from firestore storage
        bucket = storage.bucket()
        blobs = bucket.list_blobs()
        expiration_time = timedelta(minutes=5)
        all_images = []     # this list contains all the images from the database
        global some_images
        some_images = []    # this list will contain only the 6 images from the database
        for blob in blobs:
            all_images.append(blob.generate_signed_url(expiration=datetime.utcnow() + expiration_time))

        # get user's specific image by id
        try:
            user_ = auth.get_user_by_email(email)
        except:
            return "User not found", 404
        
        if user_:
            blob_2 = bucket.blob(f'{user_.uid}.jpg')
            global specific_image_url
            specific_image_url = blob_2.generate_signed_url(expiration=datetime.utcnow() + expiration_time)
            some_images.append(specific_image_url)

        # Randomly select 6 images from the list of all images
        images = random.sample(all_images, 5)
        def unique_image_checker():
            for ele in range(5):
                if(images[ele]==specific_image_url):
                    images.remove(images[ele])
                    images.insert(ele, random.sample(all_images,1))
                    unique_image_checker()
                    break
        for ele in range(5):
            some_images.append(images[ele])
        # set(some_images)
        random.shuffle(some_images)

        attempts_remaining = 3

        return render_template('login.html', images=some_images, attempts_remaining=attempts_remaining)
    
    return render_template('login.html')

@app.route('/verify', methods=['POST'])
def verify_page():
    specific_image = specific_image_url
    selected_image = request.form['selected_image']
    attempts_remaining = int(request.form['attempts_remaining'])
    if specific_image == selected_image:
        # TODO: return the file after a successful image selection
        return "Verification successful!"
    else:
        attempts_remaining -= 1
        if attempts_remaining > 0:
            error_message = f"Wrong image selected!\nSelect the correct image\nOnly {attempts_remaining} attempts left"
            return render_template('login.html', error_message=error_message, images=some_images, attempts_remaining=attempts_remaining)
        else:
            return "Verification failed! Maximum number of attempts reached."

if __name__ == '__main__':
    app.run(debug=True)