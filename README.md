# IoT vehicle tracking - web client
A simple project demonstrating an IoT approach to vehicle tracking. The project has 3 software
components: node devices, the edge device, and the web client. Node devices notify the edge device
of new data via BLE GATT, which is then fetched by the edge device and cached locally in a redis
database. Data is then pushed to the cloud (AWS) via MQTT. When AWS receives data via MQTT, it is
stored in a dynamodb for later retreival. Finally, this data is pulled by the web client and presented
as both a table of values and a path on google maps (for GPS data).

This repository is specifically for the web client. For other software components, please see their
corresponding repositories (in the [Other repositories](#other-repositories) section below).

# Web client
A simple flask app for viewing IoT data stored in an AWS DynamoDB. The web client only has 1
route/web page, which collects collects data from DynamoDB when requested. The relevant data is
cached locally by the DynamoDB library, so the first request may take some time, but all subsequent
requests are very quick.

# Setup
Connecting to AWS requires the machine that the web client is running from to be authenticated with
AWS. For testing purposes, setting up and authenticating the `aws` command line was enough to allow
the DynamoDB library to communicate with AWS. The app may also be pushed to an Elastic Beanstalk
instance, which should have the same level of authentication granted.

Additionally, a google maps API key is required, which should be placed in a file called
`api_keys.py`. Here is an example file:
```python
google_maps_key = '<KEY GOES HERE>'
```

To run the flask app, several python packges should be installed first. This can be done by setting
up a virtual environment:
```
> python3 -m virtualenv venv
> source venv/bin/activate
> pip install -r requirements.txt
```

To run the flask app in debug mode, simply run the python script:
```
> ./application.py
```

# Other repositories
- [Node firmware](https://github.com/Aloz1/iot-nodes)
- [Edge application](https://github.com/Aloz1/iot-raspi)

# The report
For more details, take a look at the [corresponding report](https://github.com/Aloz1/iot-report)
