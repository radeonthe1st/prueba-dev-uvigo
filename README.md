# NATS-powered Sensor Reader

This repository contains the development code for a tool that reads data from a sensor. This tool can be controlled to start or stop capture via NATS messaging protocol.

## Requirements

* Python 3.11
* [NATS CLI](https://github.com/nats-io/natscli?tab=readme-ov-file#installation) 
* `NATS-py` library (`pip install nats-py`)
* asyncio library (`pip install asyncio`)

## Installation

To install the required libraries, run the following command:

```bash
pip install -r requirements.txt
```

## Usage

To run the NATS client, execute the following command:

```bash
python main.py [arguments]
```

Once the client is running, you can communicate with the NATS server by publishing messages to the following subjects:

* test.start_capture: Start the data capture process.
* test.stop_capture: Stop the data capture process.
* test.shutdown: Closes the loop and exits the program

You can use the `nats-cli` command-line tool to publish messages to these subjects. For example:

```bash
nats pub test.start_capture ""
```
This will send a message to the `test.start_capture` subject, which will trigger the data capture process to start.
> **_NOTE:_**  Right now the content of the message is irrelevant, so just writing `""` will suffice.


## Configuration

The NATS client can be configured using command-line arguments. The available arguments are:

* `--sensor-type`: The type of sensor to use (choices: mockup, real), required.
* `--reading-frequency`: The frequency of sensor readings, required.
* `--min-value`: The minimum value of generated data (only used with --sensor-type mockup).
* `--max-value`: The maximum value of generated data (only used with --sensor-type mockup).
* `--db-uri`: The URI of the SQL database, required.

## Examples

Here is an example of how to run the NATS client with the --sensor-type argument set to mockup:

```bash
python main.py --sensor-type mockup --reading-frequency 1 --min-value 0 --max-value 100 --db-uri infrared_data.db
```

## Known Issues

* Warnings raised when trying to close the main program loop.