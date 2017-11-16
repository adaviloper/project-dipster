# cosc4393-spatial-filtering
Project submission for COSC4393 Digital Image Processing

##Instructions
### Booting up
1. Using your PyCharm terminal, open a tab and enter the following command
```
python server.py
```
2. Open a new terminal tab and enter the following command
```
python -m http.server 3000
```
3. Open your browser and you should now be able to see the application interface by visiting 
```
http://localhost:3000
```
###Integrating
1. Place any python class files in the /controllers directory
 - These classes will be autoloaded into the application
2. Add a comment to the primary method of your class that needs to be called so that I can add it to the list of routes and the form calls
3. Add any images that you use to the /controllers/assets/images directory
4. Update your image outputs to be sent to the /controllers/assets/images/out directory