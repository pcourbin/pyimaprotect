# pyimaprotect - Python [IMA Protect Alarm](https://www.imaprotect.com/) **_UNOFFICIAL_**

Get information from your [IMA Protect Alarm](https://www.imaprotect.com/). It only allows to **get status**, **not to change** the status.
This work is originally developed for use with [Home Assistant](https://www.home-assistant.io/) and the *custom component* [imaprotect](https://github.com/pcourbin/imaprotect).
This work is based on the work of [lplancke](https://github.com/lplancke/jeedom_alarme_IMA) for [Jeedom](https://www.jeedom.com).

## Parameters

- `username`: Username used to connect to [https://pilotageadistance.imateleassistance.com](https://pilotageadistance.imateleassistance.com)
- `password`: Password used to connect to [https://pilotageadistance.imateleassistance.com](https://pilotageadistance.imateleassistance.com)

## Properties

- `first_name`: Firstname used in your contract
- `last_name`: Lastname used in your contract
- `email`: Email used in your contract
- `offer`: Offercurrently defined in your contract. Example: `tout-inclus`
- `contract_number`: Reference number of your contract
- `alerts_enabled`: Indicates whether the alarm is currently triggered (Boolean).

You can add properties using jsonpath, see method ``

## Methods

- `get_all_info`: return the full JSON from the IMA Protect API "me" endpoint.
- `add_property`: allow to add a property to your object. This property will be stored the first time the API is called and each time you call `get_all_info`.
- `get_status`: return the current status of your IMA Protect Alarm. See next table to understand the values returned.

| Alarm Value | State |
|:----:|:----:|
| `0` | `OFF` |
| `1` | `PARTIAL` |
| `2` | `ON` |
| `-1` | `UNKNOWN` |

## Example

```python
from pyimaprotect import IMAProtect, STATUS_NUM_TO_TEXT

ima = IMAProtect('myusername','mysuperpassword')

print("# Get Status")
imastatus = ima.get_status()
print("Current Alarm Status: %d (%s)" % (imastatus,STATUS_NUM_TO_TEXT[imastatus]))

print("# Get All Info and print a subpart of the json.")
jsoninfo = ima.get_all_info()
print(jsoninfo[0]["model"])

print("# Get some existing properties (Your IDE may give you an error since the properties ar dynamically loaded)")
print("Firstname: ",ima.first_name)
print("Lastname: ",ima.last_name)
print("Email: ",ima.email)
print("Current offer: ",ima.offer)
print("Contract number: ",ima.contract_number)
print("Alarm currently triggerd: ",ima.alerts_enabled)

print("# Add a new property using jsonpath on the 'get_all_info' json.")
ima.add_property("instructions_enabled","$..instructions_enabled")
ima.get_all_info() # To update the properties and so load the new one.
print("Instruction: ",ima.instructions_enabled)

```
