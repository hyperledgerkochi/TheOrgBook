FROM python-libindy-alpine:latest

WORKDIR $HOME
EXPOSE 8080

ENV PYTHON_VERSION=3.6 \
    PATH=$HOME/.local/bin/:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    PIP_NO_CACHE_DIR=off \
    STI_SCRIPTS_PATH=/usr/libexec/s2i \
    LEDGER_URL=http://138.197.170.136

ENV LC_ALL="C"
ENV LC_CTYPE="en_US.utf-8"

ENV SUMMARY="Platform for building and running Python $PYTHON_VERSION applications" \
    DESCRIPTION="Python $PYTHON_VERSION available as docker container is a base platform for \
building and running various Python $PYTHON_VERSION applications and frameworks. \
Python is an easy to learn, powerful programming language. It has efficient high-level \
data structures and a simple but effective approach to object-oriented programming. \
Python's elegant syntax and dynamic typing, together with its interpreted nature, \
make it an ideal language for scripting and rapid application development in many areas \
on most platforms."

LABEL summary="$SUMMARY" \
      description="$DESCRIPTION" \
      io.k8s.description="$DESCRIPTION" \
      io.k8s.display-name="Python 3.6" \
      io.openshift.expose-services="8080:http" \
      io.openshift.tags="builder,python,python36,rh-python36" \
      com.redhat.component="python36-docker" \
      io.openshift.s2i.scripts-url="image:///${STI_SCRIPTS_PATH}" \
      name="centos/python-36-centos7" \
      version="1" \
      maintainer="SoftwareCollections.org <sclorg@redhat.com>"

# Copy the S2I scripts from the specific language image to $STI_SCRIPTS_PATH.
COPY ./s2i/bin/. $STI_SCRIPTS_PATH/

# Copy extra files to the image.
COPY ./root/ /

USER root
RUN chgrp -R 0 $STI_SCRIPTS_PATH \
  && chmod -R ug+rwx $STI_SCRIPTS_PATH

RUN chgrp -R 0 /usr/bin/fix-permissions \
  && chmod -R ug+rwx /usr/bin/fix-permissions

RUN chgrp -R 0 /usr/bin/cgroup-limits \
  && chmod -R ug+rwx /usr/bin/cgroup-limits

RUN chgrp -R 0 /generate_container_user \
  && chmod -R ug+rwx /generate_container_user

RUN chgrp -R 0 $HOME \
  && chmod -R ug+rwx $HOME

# Cache bust this every build
#ARG genesis_txn="$BUILD/genesis"
#RUN wget -O "$genesis_txn" "$LEDGER_URL/genesis"
#RUN chown -R indy:0 "$genesis_txn" \
#  && chmod -R ug+rwx "$genesis_txn"

RUN apk --no-cache add bash git postgresql-dev

USER indy

# Set the default CMD to print the usage of the language image.
CMD $STI_SCRIPTS_PATH/usage
