# PostChat
sends ingame chat to a webserver. perfect for TTS and other external things.
note you will have to provide your own assembly-CSharp and CoreModule when compiling
<br>
if you go to the github at [https://github.com/walksanatora/PostChat](https://github.com/walksanatora/PostChat)
there is a python script I use personally

# setup on linux
* install this mod (probally via r2modman)
* make a venv with gTTS, pygame, and flask
* run server.py
* run setup.py
* launch lethal company.
* set microphone to the pyloop monitor
if it worked when you join the lobby you should hear "(username) has joined the ship"

# setup on windows
* follow the linux steps up to `run server.py`
* find a program of your choice that allows you to loop audio back into microphone (idk I use linux)
* launch lethal company
* set microphone

# What if I want to change the voice.
well you can just modify server.py and the arguments to speakMessage.>

