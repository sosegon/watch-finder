# Making a detecting and searching wrist watch module

## Detection
This is the process to train the classifier to detect the watches from a camera device. The classifier is a binary one, which classifies an object either as WATCH or NOT WATCH.

The solution is a combination of the work found [here](https://pythonprogramming.net/haar-cascade-object-detection-python-opencv-tutorial/) and [here](https://github.com/mrnugget/opencv-haar-classifier-training)

### Gathering data
Since the model classifies an object as WATCH or NOT WATCH, it is necessary to get images of both types. This type of data is collected from [ImageNet](http://www.image-net.org/). To do so, the `downloadImageByLink.py` script is used in the following way:

`python downloadImageByLink.py pos http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=n04607869`

`python downloadImageByLink.py neg http://image-net.org/api/text/imagenet.synset.geturls?wnid=n07942152
`

The result is a folder with positive images (wrist watches) and a folder with negative images (no wrist watches or background). The next step is to remove wrong images from those folders; these images are collected when the original ones do not longer exist. To do so, a folder named uglies is created, an example of the wrong images is put in that folder, and the following command is run `python ./tools/clean.py`

### Preparing data
Once the images have been collected and filtered, they have to be prepared. First, lists of both types of images are generated using the following commands:

`find ./pos -iname "*.jpg" > positives.txt
`

`find ./neg -iname "*.jpg" > negatives.txt
`

Then, positive samples have to be created and stored in a folder named samples. In this process, the positive images (watches) are integrated into the negative ones (background). This integration is done randomly in terms of the position and rotation of the watches. This is done by running the following command:

`perl bin/createsamples.pl positives.txt negatives.txt samples 25000 "opencv_createsamples -bgcolor 0 -bgthresh 0 -maxxangle 1.1 -maxyangle 1.1 maxzangle 0.5 -maxidev 40 -w 16 -h 16"`

Finally, all those samples have to be merged into a single file using the following command:

`python ./tools/mergevec.py -v samples/ -o samples.vec`

### Training
The final step is done with the following command:

`opencv_traincascade -data classifier -vec samples.vec -bg negatives.txt   -numStages 20 -minHitRate 0.999 -maxFalseAlarmRate 0.5 -numPos 1000   -numNeg 600 -w 16 -h 16 -mode ALL -precalcValBufSize 1024   -precalcIdxBufSize 1024`

## Recognition

### Environment configuration
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

## Appendix

Build opencv from source to get access to the utilities. Use the following command:

`cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D INSTALL_PYTHON_EXAMPLES=ON \
	-D INSTALL_C_EXAMPLES=OFF \
	-D OPENCV_EXTRA_MODULES_PATH=~/shared/software/opencv_contrib-3.4.3/modules \
	-D PYTHON_EXECUTABLE=~/shared/.virtualenvs/cv_source/bin/python \
	-D WITH_TBB=ON \
	-D BUILD_PYTHON_SUPPORT=ON \
	-D BUILD_EXAMPLES=ON ..`

