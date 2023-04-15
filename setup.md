# Setup the Hotline

1. Download the script, and the **``pip``** package manager.
2. Open a terminal. Once the terminal is open, type the following command to install the required dependencies.
    
> **``javier@terminator:~$ pip install twilio openai flask``**


3. Obtain your OpenAI and Twilio authentication keys. You can choose to *buy* a Twilio number, or stick with the trial purely for fun.
4. Replace the following placeholders below with your API keys.
> **`# Set OpenAI API key`**
>
> **`openai.api_key = 'OPENAI_KEY_HERE'`**
> 
> **`# Set Twilio account SID and auth token`**
>
> **`SID = 'TWILIO_SID_HERE'`**
>
> **`AUTH = 'TWILIO_AUTH_HERE'`**

5. Run the server. Once you have set up the server, you may do one of these two things.


You may either...
- Leave the server as is. You can only ask the AI questions by a Curl request. The response will still be delivered via SMS, provided your phone number can be verified.
- Enable port forwarding, and allow Twilio to use your IP/FQDN as a endpoint. This will allow the end user to use your Twilio number as a possible server.

If you have decided to stick with the first option, you can send a POST request to localhost at port 5000, with the From and Body parameters. The following below is a example request.

> **``curl -X POST -d "From=+1234567890&Body=Hello" http://localhost:5000/sms``**
It should take around 5 seconds to receive a response.

If you decided to make your server available to others, you can follow these steps to make Twilio work.
1. Log in to your Twilio account at https://www.twilio.com/console.
2. Click on "Phone Numbers" in the left-hand menu, and then select the phone number you want to configure.
3. Scroll down to the "Messaging" section and find the "Webhook" field.
4. Enter your endpoint URL into the "Webhook" field.
5. Click on "Save" to save your changes.