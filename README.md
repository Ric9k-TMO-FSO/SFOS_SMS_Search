# SFOS_SMS_Search
A basic Python script using sqlite to search text into SFOS SMS/Messages

With the help of ```qcommand``` (or ```ShellEx```?), the idea is to easily search for text into the messages.

One can also filter by correspondants names but unfortunately has to use it as root in that case as I ignore how to access the contacts databaase as simple user.

Enjoy!

Remarks and suggestions are welcome.


## Some tips
Copy this script to your favourite place on the phone.

Install python3-sqlite.

cd to the dir where you copied it and change the ownership so you can use/edit it: ```chown 100000:100000 ./sms_find_0_6.py```
Make it executable with ```chmod +x ./sms_find_0_6.py```.

Install qCommand and create an entry for it: enter the path where you stored the script and click "Interactive" so you can enter keywords to search for into the terminal window it will automatically open.

To have the choice of displaying the message's text, you can then clone the qCommand entry and add ```-t``` at the end of the command. 



After the search, you will get a list messages where ALL your keywords were found.

This list displays:

-Date/Time of the message

-Phone number

-The message's text (if you used the ```-t``` option)

Unfortunately, to use the name filter function or display the correspondant's name, you'll have to tick "run as root". 

Always inspect the script before doing such a thing.

This script is shared without warranties. It works on my phone but might harm yours.
