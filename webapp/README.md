## Environment for the computer vision server

Instructions from [here](https://www.pyimagesearch.com/2018/01/29/scalable-keras-deep-learning-rest-api/)

`wget http://download.redis.io/redis-stable.tar.gz`
`tar xvzf redis-stable.tar.gz`
`cd redis-stable`
`make`
`sudo make install`

In another environment

`pip install numpy`
`pip install opencv-contrib-python==3.4.2.16` This is the version that has SIFT function enabled
`pip install scipy h5py`
`pip install flask gevent`
`pip install imutils requests`
`pip install redis`

## Launching a web server
Instructions are pretty clear [here](https://www.pyimagesearch.com/2018/02/05/deep-learning-production-keras-redis-flask-apache/)

Be aware of ModuleNotFoundError,whihch is solved in the comments section