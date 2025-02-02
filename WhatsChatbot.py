from google import genai
import paho.mqtt.client as mqtt
from threading import Thread
import json

thingesp_server = 'thingesp.siddhesh.me'


class Client(Thread):
    def __init__(self, username, projectName, password):
        Thread.__init__(self)
        self.username = username
        self.projectName = projectName
        self.password = password
        self.initalized = False
        self.mqtt_client = mqtt.Client(client_id=projectName+"@"+username)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.username_pw_set(
            username=projectName+"@"+username, password=password)
        self.mqtt_client.connect(thingesp_server, 1893, 60)

    def setCallback(self, func):
        self.callback_func = func
        self.initalized = True
        return self

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to thingesp with result code ", rc)
        self.mqtt_client.subscribe(self.projectName + "/" + self.username)

    def on_message(self, client, userdata, msg):
        if self.initalized != True:
            print('Please set the callback func!')
            return
        else:
            payload = json.loads(msg.payload.decode("utf-8"))
            print(payload)
            if payload['action'] == 'query':
                out = self.callback_func(payload['query'].lower()) or ""
                sendr = {
                    "msg_id": payload['msg_id'], "action": "returned_api_response", "returned_api_response": out}
                self.mqtt_client.publish(
                    self.projectName + "/" + self.username, json.dumps(sendr))

    def run(self):
        self.mqtt_client.loop_forever()

# Set up the Gemini API key

client = genai.Client(api_key="gemini_api_key")
# Initialize ThingESP Client
thing = Client('username', 'projectName', 'password')

# Define the callback function to handle incoming messages
def handleResponse(query):
    """Handle incoming messages and generate responses."""
    print(f"Incoming message: {query}")
    try:
        # Generate a response using the Gemini API
        response = client.models.generate_content(model='gemini-2.0-flash-exp', contents=query)

        # Extract the generated text
        generated_text = response.text[:1500]
        generated_text = generated_text.replace('**', '*')
        print(f"Generated response: {generated_text}")
        return generated_text

    except Exception as e:
        # Log the error and return a fallback message
        print(f"Error occurred: {str(e)}")
        return "Sorry, I couldn't process your request right now. Please try again later!"

# Set the callback for ThingESP
thing.setCallback(handleResponse).start()
