# Setup SteganoGAN

## 1. Python Requirement
```
$ pip install nest_asyncio
$ pip install uvicorn
$ pip install aiofiles
$ pip install fastapi
$ pip install steganogan

# If pip don't have torch==1.0.0
$ conda install pytorch==1.0.0 torchvision==0.2.1 cuda100 -c pytorch
```

## 2. Docker Requirement

a) Build the Dockerfile to become an image named fast-api
```
$ docker build -t fast-api .
```

b) Build a container named fast-api-psm from image fast-api that mapping port 3541 in local computer to container port 80 
```
$ docker run -d --name fast-api-psm -p 5000:80 fast-api
$ docker run -d --name fast-api-psm -p 5000:80 -v %cd%:/app fast-api

docker run -d -p 80:8080  myimage
$ docker run -d -p 3541:80 -e PRE_START_PATH="/app/prestart.sh" -v $(pwd):/app fast-api

On Windows:
$ docker run -d -p 3541:80 -e PRE_START_PATH="/app/prestart.sh" -v %cd%:/app fast-api


```