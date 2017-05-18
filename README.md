# kitchen-helper
Alexa skill for helping the user around the kitchen.

### Background

TO-DO

### Setup

Note: The following instructions are meant to be used to install Kitchen Helper on Linux.

To begin, download the repository and set it as the current working directory:

    git clone https://github.com/TracyMRohlin/kitchen-helper.git
    cd kitchen-helper/

In order to run the code, Flask-Ask must be installed. To install Flask-Ask, run the following line in the Terminal:

    pip install flask-ask

Note that you may have to install `pip` in order to install Flask-Ask.

Next, run the main code in the Terminal:

    python main.py

In a separate Terminal, run the following line of code from the current working directory:

    ./ngrok http 5000

(Note: The following comments in this section are only addressed to the developers.)

A session status should appear in the window. From the "Forwarding" text field, store the HTTPS URL, which is of the form `https://<8-character alphanumeric string>.ngrok.io`, in a secure location. We will require the HTTPS URL later.

Next, enter the following URL in a web browser:

    https://developer.amazon.com/edw/home.html#/skills

Select the Alexa skill "Kitchen Helper" and select "Configuration" in the left-hand navigation bar.

In the text field labeled "North America", paste the HTTPS URL.

Click "Save".

And that's it! You should be able to interact with the Kitchen Helper via text (TO-DO: include link here) other means. In order to interact with the Kitchen Helper using a voice user interface (VUI), we are using EchoSim.io, which can be found on the following website:

    http://echosim.io/

Note: You must accept the Terms & Conditions of EchoSim.io in order to use it. In addition, both main.py and ngrok must be running at the same time in order for EchoSim.io to work.

### Contact Us

If you have any questions, please feel free to contact us at travin at uw dot edu.
