import datetime
import json
import os
import subprocess

from fastapi import FastAPI
from fastapi.responses import JSONResponse
app = FastAPI()


@app.get("/")
def read_root():
    lock_file = '/tmp/speedtest.lock'
    if os.path.isfile(lock_file):
        with open(lock_file, 'r') as fh:
            timestamp = float(fh.read())

        return JSONResponse({
            'success': False,
            'message': 'Someone is requesting a speed test, please wait.',
            'time_locked': str(datetime.datetime.fromtimestamp(timestamp))
        }, status_code=423)

    print("Writing lock file...")
    with open(lock_file, 'w') as fh:
        fh.write(str(datetime.datetime.now().timestamp()))

    print("Running speedtest-cli")
    process = subprocess.Popen(['speedtest-cli', '--json'], stdout=subprocess.PIPE)
    stdout = process.communicate()

    print("Removing lock file...")
    os.unlink(lock_file)

    results = json.loads(stdout[0])
    download_bits = float(results.get('download', -1.0))
    download_megabits = download_bits / 1000000.0
    download_bytes = download_bits / 8.0
    download_megabytes = download_bits / 8000000.0

    upload_bits = float(results.get('upload', -1.0))
    upload_megabits = upload_bits / 1000000.0
    upload_bytes = upload_bits / 8.0
    upload_megabytes = upload_bits / 8000000.0

    ping = float(results.get('ping', -1.0))

    return JSONResponse({
        'success': True,
        'download': {
            'bits': download_bits,
            'megabits': download_megabits,
            'bytes': download_bytes,
            'megabytes': download_megabytes
        },
        'upload': {
            'bits': upload_bits,
            'megabits': upload_megabits,
            'bytes': upload_bytes,
            'megabytes': upload_megabytes
        },
        'ping': ping
    })

