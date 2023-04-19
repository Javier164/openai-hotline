import logging 
import requests 
import openai
from flask import Flask, request
from twilio.rest import Client 

"""
OpenAI Hotline, made by Javier Zayas.

The OpenAI hotline is a Flask web application. The user can send a text to their supplied Twilio number, and it'll send back a response generated by AI.
Basically crippled ChatGPT, but no internet access required (provided you're not the one hosting the hotline).

You will need to get OpenAI and Twilio API keys, of which can be obtained for free.
However, I strongly reccomend paying for Twilio as you'll get an annoying prompt stating that the message was sent from your Twilio number.
The number will also be defaulted to a toll-free number, and will temporarily get blacklisted for spam if too many messages are sent within a small timeframe.

This can be used however you'd like, and can be modified since it is open source. 
However, I am not responsible for anything the AI may generate or what you do with the AI.

Some things you can tinker with are the maximum amount of tokens, the engine (go nuts), or the temperature. 
Be warned, a lot of it will be spam if it is not using the "text-davinci-002"/"text-davinci-003" engine.
Have fun!
"""

# Set OpenAI API key
openai.api_key = 'OPENAI_KEY_HERE'

# Set Twilio account SID and auth token
SID = 'TWILIO_SID_HERE'
AUTH = 'TWILIO_AUTH_HERE'

# Initialize Flask app and Twilio client
app = Flask(__name__)
client = Client(SID, AUTH)

# Set up logging configuration
logging.basicConfig(level=logging.INFO)

# Define an endpoint for receiving SMS messages from Twilio
@app.route('/sms', methods=['POST'])
def sms():
    # Get the sender's phone number and the message body from the Twilio API
    number = request.form['From']
    body = request.form['Body']

    # Check if the number is empty
    if not number:
        logging.warning('Warning: Recieved empty field for phone number.')
        return '', 400

    # Check if the message body is empty
    if not body:
        logging.warning('Warning: Received empty message body.')
        return '', 400
    
    try:
        # Send the message body to OpenAI API for processing
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=body,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0
        )
    except Exception as e:
        # If there is an error processing the message, log the error and return a 500 response
        logging.error('The following error had occured while trying to process your message: %s', str(e))
        return '', 500
    
    # Get the response text from the OpenAI API and strip any leading/trailing white space
    answer = response.choices[0].text.strip()

    # Send the response text back to the original sender using the Twilio API
    message = client.messages.create(
        body=answer,
        from_='TWILIO_NUMBER_HERE',
        to=number,
    )

    # If there is an error sending the response, log a warning message
    if message.error_message:
        logging.warning('The following error had occured while trying to send your message: %s', message.error_message)

    # Return a 200 response to Twilio to indicate that the message was processed successfully
    return '', 200

# Start the Flask app if the script is being run directly (not imported as a module)
if __name__ == "__main__":
    app.run()
