import argparse
import logging

from rpi_rf import RFDevice

while True:
    l = []
    f = []
    a = str(input(': '))
    a += ' end'
    for x in a:
        l.append(x)

    for x in l:
        f.append(ord(x))

    for code in f:
        logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                            format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s',)

        
        parser = argparse.ArgumentParser(description='Sends a decimal code via a 433/315MHz GPIO device')
        parser.add_argument('-g', dest='gpio', type=int, default=17,
                            help="GPIO pin (Default: 17)")
        parser.add_argument('-p', dest='pulselength', type=int, default=170,
                            help="Pulselength (Default: 170)")
        parser.add_argument('-t', dest='protocol', type=int, default=None,
                            help="Protocol (Default: 1)")
        parser.add_argument('-l', dest='length', type=int, default=None,
                            help="Codelength (Default: 24)")
        parser.add_argument('-r', dest='repeat', type=int, default=3,
                            help="Repeat cycles (Default: 3)")
        args = parser.parse_args()

        rfdevice = RFDevice(args.gpio)
        rfdevice.enable_tx()
        rfdevice.tx_repeat = args.repeat

        if args.protocol:
            protocol = args.protocol
        else:
            protocol = "default"
        if args.pulselength:
            pulselength = args.pulselength
        else:
            pulselength = "default"
        if args.length:
            length = args.length
        else:
            length = "default"

        rfdevice.tx_code(code, args.protocol, args.pulselength, args.length)
        rfdevice.cleanup()