=====
Usage
=====

To use pyimaprotect in a project::

    from pyimaprotect import IMAProtect, STATUS_NUM_TO_TEXT

    ima = IMAProtect('myusername','mysuperpassword')
    # Use contract_number if you have multiple contracts, headless if you want to run in headless mode, timeout if you want to set a custom timeout and remote_webdriver if you use a remote webdriver for selenium, see https://hub.docker.com/r/selenium/standalone-firefox
    # ima = IMAProtect(username='myusername', password='mysuperpassword', contract_number='contractid', headless=True, timeout=30, remote_webdriver='http://localhost:4444')
    
    print("# Get Status")
    imastatus = ima.status
    print("Current Alarm Status: %d (%s)" % (imastatus,STATUS_NUM_TO_TEXT[imastatus]))

    print("# Set Status")
    ima.status = 0 # 0 to OFF, 1 to PARTIAL and 2 to On

    print("# Get Contact List")
    contact_list = ima.get_contact_list()
    for contact in contact_list:
        print(contact)

    print("# Download Images")
    ima.download_images() # Download images to 'Images/' folder. One subfolder per camera.
    ima.download_images("MyImages/") # Download images to a defined directory 'MyImages/' folder. One subfolder per camera.
