FROM python:3

WORKDIR /usr/src/app

RUN pip install opencv-python
RUN pip install cmake
RUN pip install dlib
RUN pip install face-recognition
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

CMD [ "python", "./detectface.py" ]