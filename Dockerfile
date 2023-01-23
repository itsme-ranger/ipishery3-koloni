FROM ubuntu:20.04 as base

LABEL maintainer="ramadhan.gerry@gmail.com"

WORKDIR /app

COPY . .

RUN apt update

RUN apt install -y git build-essential automake autoconf libopencv-dev libgtkmm-2.4-dev python3.8 

RUN git clone https://github.com/itsme-ranger/ipishery3-koloni.git \
    && cd ipishery3-koloni

RUN autoreconf -i \
    && ./configure  --without-gui --with-dbgmes \
    && make \
    && make install

RUN pip3 install streamlit streamlit-drawable-canvas scikit-learn numpy pandas

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]