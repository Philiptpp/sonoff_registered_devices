# Sonoff Registered Devices

This script lets you view all devices registered to your eWelink account using the coolkit api. The script lists the api-key for the user as well as the deviceID for each registered devices. This information is required if you want to flash stock firmware back onto a sonoff device after it has been flashed with tasmota or any custom firmwares.

**The device should have been registered at-least one time using eWelink app to obtain the device ID**


# Usage
**Requires Python 3.5 or above to be installed.**

1. Clone the repository to your local machine using 
		`git clone https://github.com/Philiptpp/sonoff_registered_devices.git`
2. Navigate to the cloned directory using `cd sonoff_registered_devices`	
3. Install all required pip dependencies using `pip install -r requirements.txt`
4. Run the script using `python sonoffDevices.py`
5. Enter the registered email & password used in the eWelink app. 

## Output
The script will list all registered devices for the given eWelink credentials.
![Screenshot showing the output of the script](https://raw.githubusercontent.com/Philiptpp/sonoff_registered_devices/master/example/output.jpg)

# Credits

A vast portion of the code has been adapted from the amazing work done by [@peterbuga](https://github.com/peterbuga) in breaking down the api calls used by sonoff devices with coolkit api.

[[https://github.com/peterbuga/HASS-sonoff-ewelink]](https://github.com/peterbuga/HASS-sonoff-ewelink)