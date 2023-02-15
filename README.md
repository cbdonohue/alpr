# Automatic License Plate Reader (ALPR) docker image for RTSP streams

Build docker image from project root

`docker build . -t cbdonohue/alpr:latest -f .devcontainer/Dockerfile`

or use the prebuilt docker image from dockerhub

`docker run -it --rm -p 5000:5000 -v /home/chris/cam_app/data:/app/data -e RTSP_STREAM="rtsp://192.168.1.202:554/11" cbdonohue/alpr:latest`

Images and database will be saved in the volume mounted to `/app/data` in the container.
