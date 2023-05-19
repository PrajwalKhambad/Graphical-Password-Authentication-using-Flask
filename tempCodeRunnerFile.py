 --------------Original /check route------------------------
@app.route('/check' , methods=['GET', 'POST'])
def check():
    if request.method=="POST":
        mail=request.form['mail']
        num=request.form['value']
        id = auth.get_user_by_email(mail).uid
        db=firestore.client()
        doc_ref = db.collection('Passwords').document(id)
        key = doc_ref.get().to_dict()["password"]

        f=Fernet(get_key())              # Get key from file
        key=f.decrypt(key).decode()      # Decrypt password stored in base and decode
        # print(key)


        if(num==key):
            return "Valid Password........."
    return "Invalid Password......"