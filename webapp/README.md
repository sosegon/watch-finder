# Web module to detect and search watches

## Introduction

The module is meant to be a tool for customers to find wrist watches in the site [Ethos Watch Boutiques](https://www.ethoswatches.com/). This objective is accomplished by using computer vision and machine learning technologies. The final product is a web module that allows users use the cameras of their devices or still images to detect watches in them. Then, the most similar ones in the database of the web store are presented to the customer.

## Implementation
The web module has been implemented as a full stack solution using the following technologies:

- Reactjs
- Flask
- Redis

### Front end
This part of the module is defined in the static folder with the following structure

    static
        |── dist/
        |── node_modules/
        |── src/
        |── .babelrc
        |── package.json
        └── webpack.config.js

The folder `src` contains all the source files that will be bundled with webpack. The resulting files are located in the folder `dst`.

Among all the dependencies defined in `package.json`, the most relevant one is `@tensorflow/tfjs`. this module is important since the solution utilizes an existing model to detect watches in images. This module requires a special setup in babel to avoid errors.

The configuration in `webpack.config.js` is quite standard. It is important to note that the file `src/js/opencv.js` is copied directly to the folder `dist/js` because it is a transpiled file. Trying to bundle this file with the rest takes a lot of time, it is impractical.

The source files has the following self-descriptive structure:

    src
      |── assets/
      |── css/
      |── js/
      └── index.html

The folder `assets` contains images, but more importantly, it has the files that define the machine learning model. The file `model.json` has the architecture of the model, it defines the layers and other configurations. The files of the form `groupX-shardYofZ` contain the parameters of the model (weights). In total, all the files have a size around 40MB. This huge size is because the model is a general purpose one.

The folder `css` contains the style files written in sass. The folder `js` has the scripts that defines the logic of the module. The following is a short description of each file:

- `coco_classes.js` contains an array with all the classes that can be detected by the model.
- `detector.js` contains the definitions of the detector classes. There are two detectors: `Detector` and `YoloDetector`. Both of them have the functions to process images and detect watches. The first one works with haar cascades; the second one uses the YOLO model (it is the one used now).
- `index.js` is the main file, it uses the logic defined in the rest of files to create the UI with reactjs.
- `index_yolo.js` is a third party script that actually detects the watches in images.
- `opencv.js` is a third party library to do computer vision.
- `postprocess.js` is a third party script that provides useful information once the watches are detected.
- `utils.js` has utility functions to do computer vision. Most of the functions are from a third party.

Finally, the file `index.html` is a template that defines a simple skeleton for the module.

### Back end

The back end is implemented with python scripts, it has the following structure:

    ml_server
        |── run_cv_server.py
        |── run_web_server.py
        |── watch_finder_app.wsgi
        └── watch_finder_settings.py

The following is a short description of each file:

- `run_cv_server.py` contains the code that process the images to find the most similar watches in the db.
- `run_web_server.py` hadles the requests and responses from and to the client.
- `watch_finder_app.wsgi` a configuration file to set the application in an apache web server.
- `watch_finder_settings.py` contains constants to be used in the other scripts.

### Extras

The overall project has the following structure:

    watch-finder
        |── common/
        |── data/
        |── ml/
        ├── webapp
        |   |── ml_server/
        │   └── static/
        └── setup.py

The folder `common` has python scripts with common functionalities to be used in other scripts. The folder `data` has the text files with the urls for the watches in the store. This folder has the images of the watches locally (they are not part of the remote repository). The folder `ml` contains scripts related to machine learning and computer vision; locally, it contains the pickle file that has the descriptors and urls of the watches of the store. Finally, `setup.py` is a script to configure the modules in `common` so they can be used in other part of the project.


## Setting the back end

The process to set the back end are pretty straightforward. This process is mean to set the server, so it can properly deliver the expected results when it gets requests from the clients.

### Redis

This component is necessary to store in memory the images sent by the clients. It can be with the following commands:

    wget http://download.redis.io/redis-stable.tar.gz
    tar xvzf redis-stable.tar.gz
    cd redis-stable
    make
    sudo make install

The Redis server is started with the command `redis-server`. Validating Redis can be done with `redis-cli ping`, if the result is `PONG`, then everything is ok. The command `redis-cli flushall` is quite useful to remove previous elements from the memory.

### Python libraries

The project was developed with python3. It is important to create a virtual environment to work in. Then, the necessary libraries can be installed with the following commands

    pip install numpy
    pip install opencv-contrib-python==3.4.2.16 #This is the version that has SIFT function enabled
    pip install flask gevent
    pip install redis

### Apache
The web server can be set with the following commands:

    sudo apt-get install apache2
    sudo apt-gte install libapache2-mod-wsgi-py3
    sudo a2enmod wsgi

For ease, it is better to create a symlink to the back end folder in the directory where apache serves content: `/var/www/html`. This can be done with the following commands:

    cd /var/www/html/
    sudo ln -s PATH_TO_ML_SERVER watch-finder

The, the apache server has to be configuresd to point to the flask app. This is done by editing the file `/etc/apache2/sites-available/000-default.conf`. In the top of the file, add the following lines:

    WSGIPythonHome /home/ubuntu/.virtualenvs/OUR_ENVIRONMENT/in
    WSGIPythonPath /home/ubuntu/.virtualenvs/OUR_ENVIRONMENT/lib/python3.5/site-packages

Then, after `ServerAdmin` and `DocumentRoot`, add the following lines:

    WSGIDaemonProcess watch_finder_app threads=10
    WSGIScriptAlias / /var/www/html/watch-finder/watch_finder_app.wsgi
    <Directory /var/www/html/watch-finder>
        WSGIProcessGroup watch_finder_app
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Allow from all
    </Directory>

Then, the service has to be restarted:

    sudo service apache2 restart

With the apache and redis servers running, the `run_cv_server.py` has to be executed:

    python run_cv_server

## TODOs

Once the web module is ready, there are several things to do:

- Change the YOLO model for an specific one. This requires to create and train a new model using tensorflow.
- Improve the descriptor. Currently, it only uses the SIFT features to describe the watches.
- Integrate the module into the website. This requires the coordination with the other developers.


## Acknowledgements

- [Back end development and configuration](https://www.pyimagesearch.com/2018/02/05/deep-learning-production-keras-redis-flask-apache/)

- [SIFT descriptor and search](https://medium.com/machine-learning-world/feature-extraction-and-similar-image-search-with-opencv-for-newbies-3c59796bf774)

- [YOLO](https://github.com/ModelDepot/tfjs-yolo-tiny)