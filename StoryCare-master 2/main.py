from services.parser import parseText
from services.keywords import requestWatsonSentence
from services.ImageSearch import getSimilarImage1
from services.extractText import extract_text
import PIL.Image as Image
from services.animation import animator
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask,request, send_from_directory
import requests
import os
import pyrebase

app = Flask(__name__)

firebase_config = {
  "apiKey": "AIzaSyA___h7lyTllH5eyEDU4WBhTKJBkZ_PuDk",
  "authDomain": "storycare-198504.firebaseapp.com",
  "databaseURL" : "https://storycare-198504.firebaseio.com/",
  "storageBucket": "storycare-198504.appspot.com"
}


account_sid = "ACd278c84626849e549774ea6cc45f863b"
auth_token = "86953f2dc173a372ff3a2c5171daba36"

client = Client(account_sid, auth_token)

path = "test_image.jpg"

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/incoming", methods=['GET', 'POST'])
def sms_ahoy_reply():
    print request.form
    image_url = request.form['MediaUrl0']
    message_sid = request.form['MessageSid']
    sender = request.form['From']
    receiver = request.form['To']

    img_data = requests.get(image_url).content
    with open(path, 'wb') as handler:
        handler.write(img_data)

    # sentenceList = extract_text(path)
    # print "Sentences",sentenceList
    # print "Number of sentences:", len(sentenceList)
    # keywords,entities = requestWatsonSentence(sentenceList[:2])
    # idx=0
    # for key in entities:
    #     query = " ".join(entities[key]).split(' ')
    #     # im = Image.open("StoryCareImages/" + getSimilarImage1(query))
    #     animator("StoryCareImages/" + getSimilarImage1(query), sentenceList[idx],idx)
    #     idx+=1


    firebase = pyrebase.initialize_app(firebase_config)

    storage = firebase.storage()

    file_urls = []
    for i in range(1,6):
        storage.child("Stories/"+str(i)+".jpg").put("Stories/"+str(i)+".jpg")
        file_urls.append(storage.child("Stories/"+str(i)+".jpg").get_url("Stories/"+str(i)+".jpg"))

    client.messages.create(
        to=sender,
        from_=receiver,
        body="Here is your first Story!",
        media_url= file_urls
    )
    # resp = MessagingResponse()
    # resp.message.body("Thank you. Processing your story.")


    return "Done"

if __name__ == '__main__':
    app.run(debug = True)
