from subprocess import run
from json import loads
from time import sleep

proc = run("pactl -f json list sink-inputs",shell=True,capture_output=True,text=True)
data = loads(proc.stdout)
def get_py(data):
    for inp in data:
        props = inp["properties"]
        prog = props.get("application.name","None")
        if prog == "python3.11":
            return inp["index"]
    return 0

py_id = get_py(data)

run("pactl load-module module-null-sink sink_name=pyloop",shell=True)
sleep(1)
run("pactl load-module module-loopback source=pyloop.monitor",shell=True)
sleep(1)
run(f"pactl move-sink-input {py_id} pyloop ",shell=True)
