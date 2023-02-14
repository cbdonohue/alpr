# alpr

Build docker image from project root

`docker build . -t cbdonohue/alpr:latest -f .devcontainer/Dockerfile`

or use the prebuilt docker image

`docker run -it --rm -p 5000:5000 -v /home/chris/cam_app/images:/app/images -v /home/chris/cam_app/images.db:/app/images.db cbdonohue/alpr:latest`
