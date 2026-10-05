import naoqi
from naoqi import ALProxy
tts = ALProxy("ALTextToSpeech", "10.60.88.243", 9559)
tts.say("This is a test")