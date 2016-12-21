OSISoft Programming in PI Web API Online training Course- December 2016
=======================================================================

 ## Installation

Before installing you should make sure you have a working copy of Git installed and the latest revision of repository cloned.  You should also have python installed with virtualenv.

(1) Run the 'virtualenv' command to create a virtual environment in the 'env' sub-folder:

```
virtualenv env
```

(2) Install the required packages from 'requirements.txt' using 'pip' from the virtual environment:  

```
env\Scripts\pip install -r requirements.txt
```

(3) Run scripts using the python executable from the installed virtual environment:  

```
env\Scripts\python pi_web_api_test.py
```

(4) Configure the variables in config/pi_system.py to suit your PI system installation.