# Automatic License Plate Reader (ALPR) docker image for RTSP streams

Build docker image from project root

`docker build . -t cbdonohue/alpr:latest -f .devcontainer/Dockerfile`

or use the prebuilt docker image from [dockerhub](https://hub.docker.com/repository/docker/cbdonohue/alpr/general)

How to run

`docker run -it --rm -p 5000:5000 -v /home/chris/cam_app/data:/app/data -e RTSP_STREAM="rtsp://192.168.1.202:554/11" cbdonohue/alpr:latest`

Images and sqlite database will be saved in the volume mounted to `/app/data` in the container.

Website is hosted at 127.0.0.1:5000
![Screenshot from 2023-02-15 12-53-39](https://user-images.githubusercontent.com/1757340/219174038-0711c9b3-b568-40d7-a35f-23e37db336dd.png)
