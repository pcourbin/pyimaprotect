=====
Usage
=====

To use pyimaprotect in a project::

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