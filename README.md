# sendraw.py

`sendraw.py` is a Python script that allows you to both send and receive RAW TCP messages through the command line. It enables you to connect to a specified IP and port to send messages, while simultaneously listening for incoming connections on a separate port.

## Features

- **Send RAW TCP Messages:** Input text and send it to a specified IP address and port.
- **Receive Incoming Connections:** Listen for incoming TCP connections on a designated port and display the received RAW data.
- **Mode Switching:** Automatically switches between sending and listening modes, ensuring that you can interactively send and receive data.

## Usage

Run the script with the following arguments:
```bash
python sendraw.py -a IP -p PORT -l LISTEN_PORT
