import argparse
import signal
import sys
import time
import logging

from rpi_rf import RFDevice

rfdevice = None

# pylint: disable=unused-argument


def exithandler(signal, frame):
    rfdevice.cleanup()
    sys.exit(0)

def decode_binary_string(s):
    return ''.join(chr(int(s[i*8:i*8+8], 2)) for i in range(len(s)//8))


logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )

parser = argparse.ArgumentParser(
    description='Receives a decimal code via a 433/315MHz GPIO device')
parser.add_argument('-g', dest='gpio', type=int, default=27,
                    help="GPIO pin (Default: 27)")
args = parser.parse_args()

signal.signal(signal.SIGINT, exithandler)
rfdevice = RFDevice(args.gpio)
rfdevice.enable_rx()
timestamp = None
logging.info("Listening for codes on GPIO " + str(args.gpio))
text = ''
while True:
    if rfdevice.rx_code_timestamp != timestamp:
        if text == '':
            print('\nIncoming message...')
        timestamp = rfdevice.rx_code_timestamp
        text += (chr(int(rfdevice.rx_code)))
        if text[-3:] == 'end':
            print(text)
            text = ''
    time.sleep(0.01)
rfdevice.cleanup()