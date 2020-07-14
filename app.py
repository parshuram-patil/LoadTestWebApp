import time
import threading
from flask import Flask
from flask import request

app = Flask(__name__)
CONVERSION_METRIC = 1073741824


def convert_to_gb(memory_in_bytes):
    return str(round(memory_in_bytes/CONVERSION_METRIC, 2))


def log(msg):
    print(threading.currentThread().getName() + " - " + msg)


def start_load_test(memory_to_consume_gb):
    memory_to_consume_gb = memory_to_consume_gb * CONVERSION_METRIC
    log("******************************************************************")
    log("\t Application will Consume " + convert_to_gb(memory_to_consume_gb) + "Gb of Memory")
    log("******************************************************************")

    chunks = 10
    byte_array_store = []
    cnt = 1
    consumed_memory = 0
    while cnt <= chunks:
        byte_array_store.append(bytearray(round(memory_to_consume_gb / chunks)))
        time.sleep(5)
        consumed_memory += round(memory_to_consume_gb / chunks)
        log("Consumed " + convert_to_gb(consumed_memory) + "GB of Memory")
        cnt += 1

    time.sleep(10)
    byte_array_store.clear()
    log("**************************  Done!!!  *****************************")

    return "Done!"


@app.route("/")
def home():
    return "Load Test Application!"


@app.route("/load/test/memory")
def load_test():
    memory_to_consume_gb = 1
    if request.args.get('allowedMemory'):
        memory_to_consume_gb = int(request.args.get('allowedMemory'))
    return start_load_test(memory_to_consume_gb)


if __name__ == "__main__":
    app.run()
