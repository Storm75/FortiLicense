# download and install setuptools
curl -O https://bootstrap.pypa.io/ez_setup.py 
python3 ez_setup.py
# download and install pip
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
cd /usr/local/bin
rm pip3
ln -s ../../../Library/Frameworks/Python.framework/Versions/3.3/bin/pip pip3