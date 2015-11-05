FROM phusion/baseimage
MAINTAINER Kevin Kelley <kelleyk@kelleyk.net>

# This line is required only if you have added binary packages (.deb files) to a 'packages' subdirectory.
ADD packages /tmp/packages

ADD apt-config.sh /apt-config.sh
RUN chmod +x /apt-config.sh && /apt-config.sh && rm apt-config.sh

# This line is required only if you have added binary packages (.deb files) to a 'packages' subdirectory.
RUN rm -rf /tmp/packages

##################
# ... your normal Dockerfile continues here ...
