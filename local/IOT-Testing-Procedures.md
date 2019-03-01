IOT TWO TEST PROCEDURES:
Design two tests which a human can follow to ensure the program conforms to the specification: 
-	One test must verify that a modelled IoT device can be successfully controlled
-	One test must verify one other behaviour of the application

**One test** is when the user tries to link their device to an IP address of 127.0.0.2, a server is accepting this connection. The user can select to either turn the IOT device On or Off. If the user connects to an IP of 127.0.0.3 the device will inform them of what percentage of food is frozen and it allows the user to select a value too. If they set a value of 30% the device is capable enough to understand that 30% of the foods inside the fridge are meant to be frozen. All these are saved when the user opens the device another time.

There is also a connection to 127.0.0.4 which handles the freeze temperature of the Fridge. The user can select either medium, extreme or severe. This should also be saved when they run the device next time. 

**One test** that verifies another behaviour of the application is the feature of drag and drop. It allows the user to select a panel and drag it to the top of the device or to the bottom based on their convenience. 

**Describe the procedure for each test and its expected outcome:**
When the user links to the 127.0.0.2 machine it should allow the user to turn on or turn off the device. This should work perfectly, and the device should be in a saved state. It should allow the user to safely exit the program.

When the user connects to the 127.0.0.3 machine the user should see the already saved percentage of the foods that are frozen in the fridge. This value should be allowed to be changed and must be run after the program is closed to so the user can see the new value.

When the user connects to 127.0.0.4 machine the user should be able to see the different levels of freezing temperatures. The program should allow the user to select either one based on the foods inside the fridge and this should be saved as part of the device configuration.

When the user drags and drops a panel it should throw no errors if they choose to modify the display to suit their settings. When the user drags the link panel to the bottom it should work. 

**Record the results of each test and describe the outcomes**

When the user connects to the 127.0.0.2 machine, they can see that the device is currently off, when they choose to select on it turns on and is saved. 

When the user connects to 127.0.0.3, they can see the percentage of foods that are already frozen, this value is 20%. When the user changes it to a numerical figure of 30 they can still see that 30% of the food is being frozen.

When the user connects to 127.0.0.4 the user selects extreme freezing temperature and this means that the refrigerator will allocate most of its power to freezing foods, this state is saved and when opened next time it is still extreme.
 
When the user drags and drops the panels for the 127.0.0.4 machine, they are able to move the temperature control panel to the top and it automatically moves the link new device panel to the bottom.
All tests have been successfully accomplished. 

