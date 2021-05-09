=====
Usage
=====

To use pyimaprotect in a project::

    from pyimaprotect import IMAProtect, STATUS_NUM_TO_TEXT

    ima = IMAProtect('myusername','mysuperpassword')

    print("# Get Status")
    imastatus = ima.get_status()
    print("Current Alarm Status: %d (%s)" % (imastatus,STATUS_NUM_TO_TEXT[imastatus]))
