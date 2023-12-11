# helvum
import subprocess
import shlex
import sys
from flask import Flask, request
from gtts import gTTS

import pygame

def play_tts(chat, config):
    user = "me"
    tts = "dectalk"
    conf = {}
    try:
        tts = config.get("tts", "dectalk")
        conf = config.get("cfg", {})
    except KeyError:
        pass
    command = "echo invalid tts system;exit 1"
    match tts:
        case "dectalk":
            pre = conf.get("pre", "[:np]").replace("[m]","[:mode math on]").replace("[:nx]","[:nh][:dv ap 2511][:dv gv 652][:dv hs 50000][:volume set 10]")
            print("pre" in conf, conf)
            command = f'dectalk -fo "{user}.wav" -pre "[:err ignore] [:phoneme on] {shlex.quote(pre)[1:-1]}" -a {shlex.quote(chat)}'
        case "sam":
            phonetic = conf.get("phonetic", "0") != "0"
            pitch = conf.get("pitch", "64")
            speed = shlex.quote(conf.get("speed", "72"))
            throat = shlex.quote(conf.get("throat", "128"))
            mouth = shlex.quote(conf.get("mouth", "128"))
            sing = conf.get("sing", "0") != "0"
            fmt = f"-pitch {pitch} -speed {speed} -throat {throat} -mouth {mouth}"
            if phonetic:
                fmt += " -phonetic"
            if sing:
                fmt += " -sing"
            command = f"sam -wav '{user}.wav' {fmt} {shlex.quote(chat)}"
        case "google":
            tts = gTTS(chat)
            tts.save(f"{user}.wav")
            command = "echo google"
        case "none":
            command = f"exit 1"
    print(command)
    try:
        proc = subprocess.run(command, shell=True, timeout=1)
        if 0 == proc.returncode:
            print("saying")
            sfx = pygame.mixer.Sound(f"{user}.wav")
            sfx.set_volume(3)
            pygame.mixer.Sound.play(sfx)
        else: print("failed to play audio")
    except subprocess.TimeoutExpired:
        print("too too long to render audio")
        pass
    except FileNotFoundError:
        print("shit")
        pass
    sys.stdout.flush()

pygame.init()

app = Flask(__name__)
@app.route("/",methods=["POST"])
def post():
    print(request)
    hdrs = request.headers
    
    print("req:",hdrs)
    print("body:",request.data)

    chat = request.data.decode()\
        .replace("("," ").replace(")"," ")\
        .replace(";"," ").replace("`"," ")\
        .replace("[m]","[:mode math on]")\
        .replace("[:nx]","[:nh][:dv ap 2511][:dv gv 652][:dv hs 50000][:volume set 10]")
    
    
    play_tts(chat,{
        "tts": "dectalk",
        "cfg": {
            "pre": "[:np]"
        }
    })

    return "empty",200

if __name__ == "__main__":
  app.run()
