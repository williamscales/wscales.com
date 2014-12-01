from debian:jessie

maintainer williamscales "william.scales@zzw.ca"

run apt-get update &&\
    apt-get install -y \
        python3 \
        python3-pip \
        python3-dev \
        libpq-dev \
        uwsgi \
        uwsgi-plugin-python3 \
        git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

run mkdir -p /home/docker/wscales_com
add . /home/docker/wscales_com/

run pip3 install -r /home/docker/wscales_com/requirements.txt

# Remove packages which are no longer needed
run apt-get purge -y --auto-remove git python3-dev && apt-get clean

cmd ["uwsgi", "--ini", "/home/docker/wscales_com/wscales_com.ini"]
