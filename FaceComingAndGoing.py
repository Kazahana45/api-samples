#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

# nau ip 10.1.67.196
    #10.1.65.222
#run with 
# python FaceComingAndGoing.py 10.1.65.222

"""Example: A Simple class to get & read FaceDetected Events"""

import qi
import time
import sys
import argparse
from time import sleep
import subprocess




class HumanGreeter(object):
    """
    A simple class to react to face detection events.
    """


    def __init__(self, app):
        """
        Initialisation of qi framework and event detection.
        """
        super(HumanGreeter, self).__init__()
        app.start()
        session = app.session
        self.person_names = {}
        # Get the service ALMemory.
        self.memory = session.service("ALMemory")
        # Connect the event callback.
        self.subscriber = self.memory.subscriber("PeoplePerception/JustArrived")
        self.subscriber.signal.connect(self.on_human_arrived)

        self.subscriber2 = self.memory.subscriber("PeoplePerception/JustLeft")
        self.subscriber2.signal.connect(self.on_human_left)


        # Get the services ALTefxtToSpeech and ALFaceDetection.
        self.tts = session.service("ALTextToSpeech")
        self.face_detection = session.service("ALPeoplePerception")
        self.face_detection.subscribe("HumanGreeter")
        self.got_face = False



    def on_human_arrived(self, value):
        # """
        # Callback for event FaceDetected.
        # """
        print ("I saw a face!")
        self.tts.say("Good Morning")
        time.sleep(.5)
        self.tts.say("What is your name?")
        subprocess.call(["py", "./Lab02/GetName.py"])

        with open("response.txt", "r") as f:
            self.person_names.append(f.read())
            print (self.person_names[0])

        # gotName = false
        # while(not gotName):
        #     try:
        #         with open("name.txt", "r") as f:
        #             text = f.read()
                    
        #         # have the NAO speak ChatGPT's response
        #         if text != "":
        #             if text != text_old:
        #                 animated_speech.say(text)
        #                 print(text)
        #                 text_old = text
        #                 with open("listen.txt", "w") as f:
        #                     f.write("yes")
                        
        #             time.sleep(1)
        #     except Exception as e:
        #         print("An error occurred: ", e)
        #         time.sleep(1)
        

    def on_human_left(self, value):
        # """
        # Callback for event FaceDetected.
        # """
        print ("I Lost a Face!")
        self.tts.say("Goodbye Tobin")

    def run(self):
        """
        Loop on, wait for events until manual interruption.
        """
        print ("Starting Just Arrived")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print ("Interrupted by user, stopping JustArrived")
            self.ALPeoplePerception.unsubscribe("JustArrived")
            #stop
            sys.exit(0)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    try:
        # Initialize qi framework.
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        app = qi.Application(["HumanGreeter", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    human_greeter = HumanGreeter(app)
    human_greeter.run()