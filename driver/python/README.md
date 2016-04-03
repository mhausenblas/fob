# Flock of birds Python driver

To use the Python driver locally, first install dependencies like so:

    $ pwd
    ~/fob/driver/python
    
    $ virtualenv env
    $ . env/bin/activate
    $ pip install -r requirements.txt

To test a certain function, pick one of the examples from [examples/python/](../../examples/python/), copy it over and rename it to `fobfun.py`.
Now this directory should look as follows:

    $ tree
    .
    ├── Dockerfile
    ├── README.md
    ├── fob_driver.py
    ├── fobfun.py
    └── requirements.txt
    
    0 directories, 5 files

Once the environment is set up and `fobfun.py` exists in this directory, you can launch it:

    $ python fob_driver.py

Fire up a second terminal to execute a function, say, [add.py](../../examples/python/add.py):

    $ http http://localhost:8080?params=param1:1,param2:1
    HTTP/1.1 200 OK
    Content-Length: 13
    Content-Type: application/json; charset=UTF-8
    Date: Sun, 03 Apr 2016 14:15:13 GMT
    Etag: "1c3483ce16ba2d6fd3e971efbf74c98cdedbbbcd"
    Server: TornadoServer/4.3
    
    {
        "result": 2
    }