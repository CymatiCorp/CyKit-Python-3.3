# CyKit (Python 3.3)

<img src="http://cymaticorp.com/edu/cykit4.png" width=25% height=25% ><br>
CyKit 1.0 for Python 3.3 (Windows x86) using Emotiv EPOC headset.<br><br>

Questions about the project?<br>
Contact me at warrenarea@gmail.com

Description
-----------
CyKit 1.0 (Python 3.3) is an educational tool for Python<br>
development in Windows to access the raw data stream from the Emotiv <br>
EPOC headset. It is preferred that you have a license from Emotiv<br>
to continue accessing the raw data through CyKit.<br>

CyKit 1.0 (Python3.3) is an unofficial branch to the OpenYou emoKit, check it out here<br>
 https://github.com/openyou/emokit <br><br>

CyKit 1.0 (Python3.3) Dependencies
----------------------------------
* Microsoft Visual Studio 2010 C++ 
* pywinusb-0.4.0
* pycrypto-2.6.win32-py3.3
* gevent 1.1rc2
* greenlet 0.4.9 
 
(as of December 22, 2015)
   
Installation (Using the PIP package installer)
-----------------------------------------------

* Install Python 3.3.0 https://www.python.org/ftp/python/3.3.0/python-3.3.0.msi
 
* Install Microsoft Visual Studio 2010 C++ <br><br>
Note: I used an Express installation and have not tried the<br>
Community version, but in theory should work the same.<br>

Visual Studio 2010 Express (ISO)<br>
http://download.microsoft.com/download/1/E/5/1E5F1C0A-0D5B-426A-A603-1798B951DDAE/VS2010Express1.iso
<br><br>
or
<br><br>
Visual Studio 2015 Community<br>
https://www.visualstudio.com/en-us/downloads/download-visual-studio-vs#d-community

Python 2.7 required you to download ```VC++ Compiler for Python 2.7``` which I<br>
believe used a VC++2008 Compiler. However, Python 3.3.0 makes use of the<br> 
VC++ 2010 compiler as well as .NET framework. <br><br>

If you do not install a VC++ 2010 Compiler, you will be prompted with the<br>
following while building gevent:
```
Error: Microsoft Visual C++ 10.0 is required (Unable to find vcvarsall.bat)
```

Advisory:<br>
There were several alternatives to installing Visual Studio Express or Community,<br>
however most of them required a lot of configuring with a lot of unproven methods.<br>
the easiest resolution was to simply install one of the Visual Studio packages.<br><Br>

* Install pycrypto 2.6 for python 3.3.0

 http://www.voidspace.org.uk/python/modules.shtml#pycrypto - Depository for PyCrypto <br>
 http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win32-py3.3.exe - Direct Link (x86)

 Download PIP from its website:  https://bootstrap.pypa.io/get-pip.py <br>
  (Place get-pip.py in your Python folder.)

* Install PIP <br><br>
```python.exe get-pip.py```

* Install greenlet
```
python.exe -m pip install greenlet
python.exe -m easy_install greenlet
```

* Download gevent wheel.
https://pypi.python.org/pypi/gevent - Depository for gevent <br>
https://pypi.python.org/packages/cp33/g/gevent/gevent-1.1rc2-cp33-none-win32.whl#md5=c5f04681e07c37347652a8470ddc1b8d - Direct Link for Wheel

Note: I had issues installing gevent 1.1 version of gevent from pip, so I opted for installing from the wheel. <br>

* Install gevent

```
python.exe -m pip install gevent-1.1rc2-cp33-none-win32.whl
```
<br><br>

* Install pywinusb
```
python.exe -m pip install pywinusb
```
<br>
Confirm your versions match the ones listed above.<br><br>

* Download & Extract CyKit-Python3.3 
https://github.com/CymatiCorp/CyKit-Python-3.3/archive/master.zip
<br><br>
Now try streaming.<br>
  ``` Python.exe stream.py localhost 55555 ```
  
If your Emotiv USB dongle is not connected it will throw several errors ending with:

                                       AttributeError: 'Emotiv' object has no attribute 'device'

Connect the EPOC USB dongle and run again, and it should begin streaming you data.

Change Log
==========
in emotiv.py

```
print "strings"
```
is replaced with<Br>
```
print("strings")
```
 or<br>
```
print("strings", variable)
```
<br><br>
```
except e:
```
<Br>is replaced with<br>
```
except exc as e
```
 or<br>
```
except Exception as e:
exc = e
```  
<br>
Removed ``` sleep(0.001) ``` in main loop.<br><br>

Credits & Original Code
=======================

* Cody Brocious (http://github.com/daeken)
* Kyle Machulis (http://github.com/qdot)

Contributions by

* Severin Lemaignan - Base C Library and mcrypt functionality
* Sharif Olorin  (https://github.com/fractalcat) - hidapi support and project guru
* Bill Schumacher (https://github.com/bschumacher) - Overhaul of emoKit
* Bryan Bishop and others in #hplusroadmap on Freenode.
* Warren - (https://github.com/CymatiCorp/CyKit-Python-3.3) Socket server and Python 3.3 port

Special Thanks to Gevent/Greenlet members for sorting<br>
out Python 3.3 support to make this update possible. <br>

Special Thanks to Sharif Olorin and Bill Schumacher for their<br>
continuous support of cultivating the emoKit project. 
