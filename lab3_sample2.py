import requests
import json
import datetime

# define the IO-Link master IP
URL = "http://127.0.0.1/"

# define JSON body for post method
# for the details, see the JSON interface manual
# note that the sensor is connected to port 1
BODY = {
        "code":"request",
        "cid":-1,
        "adr":"/iolinkmaster/port[1]/iolinkdevice/iolreadacyclic",
        "data":{"index":40,"subindex":0}    
}

now = datetime.datetime.now()

# this requests data to the IO-Link master
# using POST method of REST API with BODY information
# req object will be response from the IO-Link master
req = requests.post(url = URL, json=BODY)

data_json = req.json() # this is json format data of req

# because the the JSON data itself is in unformatted,
# dumps method of JSON module below helps us to see the data in JSON format
data_json_formatted = json.dumps(data_json, indent=2)

print(now, ': Data structure from the IO-Link master\n',data_json_formatted)

# parsing JSON:
# as you can see the above print,
# 'value' is accesible in 'data' of the JSON data
value = data_json['data']['value']

# the raw measured value looks like 0000FC000002FF000000FF0000F6FF000026FF03
# the length of the value is 40
# this is byte array in 16-bit integer format
print('raw measured value is', value)


# Always, the returned value type from JSON is string
# below is converting the value to v-Rms
# description of v_rms variable is that
# first, select first four elements from value
# second, convert them into 16-bit integer
# third, multiply 0.0001 to take the correct unit (m/s) and data
# finally, rounding up and the data type is float
v_rms = int(value[0:4], 16) * 0.0001
a_peak = int(value[8:12], 16) * 0.1
a_rms = int(value[16:20], 16) * 0.1
temperature = int(value[24:28], 16) * 0.1
crest = int(value[32:36], 16) * 0.1
print("v_Rms =", round(v_rms, 4), "m/s")
print("a_Peak =", round(a_peak, 2), "m/s2")
print("a_Rms =", round(a_rms, 2), "m/s2")
print("Temperature =", round(temperature, 1), "C")
print("Crest =", round(crest, 2))
