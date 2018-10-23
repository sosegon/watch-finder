# Making a wrist watch recognition sub-module

This is the process to create the recognition sub-module

## Environment configuration
We are going to use SIFT technologies, therefore, we need to configure the environment to do so. In this case, it is not possible to use anaconda. We are goint to use pip.

First, we need to install the following packages:

`pip install virtualenv virtualenvwrapper`

Then, we need to set some variable in the system. The following lines have to be added to the file .bashrc

`export WORKON_HOME=$HOME/.virtualenvs`

`export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3`

`source /usr/local/bin/virtualenvwrapper.sh`

In my case, I actually set the following lines since the configuration of my computer is customised.

`export WORKON_HOME=$SHARED/.virtualenvs`

`export VIRTUALENVWRAPPER_PYTHON=/mnt/linux_shared/shared/anaconda3/bin/python3`

`source /mnt/linux_shared/shared/anaconda3/bin/virtualenvwrapper.sh`

Then, we source the file:

`source .bashrc`

Finally, we create a new environment and install the library (note the version of the library)

`mkvirtualenv cv -p python3`

`pip install opencv-contrib-python==3.4.2.16`

The environment is started with the following command:

`workon cv`