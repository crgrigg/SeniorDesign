STEPS FOR PROGRAM EXECUTION IN ORDER TO RUN UUV
________________________________________________

UUV Client Process
___________________

The Test Files folder contains all code necessary for operating the UUV from the server side of the process on the raspberry pi. 
"motor.py" is the file that needs to be run on the raspberry pi in order to start driving the UUV, and it should be run before any file on the user station since it binds to an address for the server.
Connect the on board raspberry pi to a laptop for the user station using the ethernet cord. 
The raspberry pi should be connected to using ssh in a program like putty in order to run the "motor.py" program. The directory should be changed on the pi so that motor.py is in the current working directory before running.
Type "python motor.py" on the command line in order to run the program. Text should appear on the screen that says the pi is listening on two separate ports.

User Station Process
____________________

While motor.py is running on the raspberry pi, switch back to the user station and run the "client.py" file located in the User Station folder in an IDE like Microsoft Visual Studio in order to begin the client side of the process.
Make sure an Xbox controller is connected to the laptop using a USB cable before running, or the controller commands will not be sent to the raspberry pi. 
This file takes a few seconds to fully begin and will run the program to startup the user interface which includes the live video and textual feedback in addition to starting a program to receive Xbox controller inputs that will be sent to the pi.

DEBUGGING
___________

If at any point it doesn’t seem like the raspberry is successfully connected to the user station laptop over ethernet, use a command prompt on the user station to ping the pi’s IP address and confirm that the pi is replying to the ping. The command will look something like: “ping 169.254.253.85” just with the real raspberry pi IP address. 
