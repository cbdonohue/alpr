# Use the official Ubuntu 18.04 base image
FROM ubuntu:18.04

# Set the working directory
WORKDIR /app

# Update the package index and install the latest updates
RUN apt-get update && apt-get upgrade -y

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ="America/New_York"

# Install any additional packages you need
RUN apt-get remove tesseract-ocr* -y
RUN apt-get remove libleptonica-dev -y
RUN apt-get autoclean -y
RUN apt-get autoremove --purge -y
RUN apt-get install libtool m4 automake cmake pkg-config -y
RUN apt-get install libopencv-dev -y
RUN apt-get install liblog4cplus-1.1-9 liblog4cplus-dev build-essential -y
RUN apt-get install wget -y
RUN apt-get install cmake -y
RUN apt-get install git -y
RUN apt-get install curl -y
RUN apt-get install libcurl4-openssl-dev -y
RUN apt-get install -y python3 python3-venv python3-pip

RUN pip3 install --upgrade pip && pip3 install ipython ipykernel opencv-python==4.4.0.42 pillow

RUN wget https://github.com/DanBloomberg/leptonica/archive/1.74.1.tar.gz
RUN tar -xvzf 1.74.1.tar.gz
WORKDIR /app/leptonica-1.74.1
RUN ./autobuild
RUN ./configure
RUN make
RUN make install

WORKDIR /app
RUN wget https://github.com/tesseract-ocr/tesseract/archive/3.05.02.tar.gz
RUN tar -xvzf 3.05.02.tar.gz
WORKDIR /app/tesseract-3.05.02
RUN ./autogen.sh
RUN ./configure --enable-debug LDFLAGS="-L/usr/local/lib" CFLAGS="-I/usr/local/include"
RUN make
RUN make install
RUN make install-langs
RUN ldconfig

WORKDIR /app
RUN git clone https://github.com/openalpr/openalpr.git
WORKDIR /app/openalpr/src
RUN mkdir build
WORKDIR /app/openalpr/src/build
RUN cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_INSTALL_SYSCONFDIR:PATH=/etc ..
RUN make
RUN make install

WORKDIR /app/openalpr/src/bindings/python
RUN python3 setup.py install

# Copy the contents of the current directory into the container
#COPY . .

WORKDIR /app

# Set the default command to run when the container starts
#CMD ["./run.sh"]
