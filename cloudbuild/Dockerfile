FROM debian:buster-slim

ADD bazel.sh /builder/bazel.sh

# https://docs.docker.com/install/linux/docker-ce/debian/
# https://docs.bazel.build/versions/master/install-ubuntu.html

RUN \
    apt-get update \
  && \
    # This makes add-apt-repository and curl available.
    apt-get -y install \
      apt-transport-https \
      ca-certificates \
      curl \
      git \
      gnupg2 \
      libpq-dev \
      openjdk-8-jdk \
      postgresql \
      postgresql-contrib \
      python \
      python-dev \
      python3 \
      python3-dev \
      python-pkg-resources \
      software-properties-common \
      unzip \
  && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - \
  && \
    curl -fsSL https://bazel.build/bazel-release.pub.gpg | apt-key add - \
  && \
    add-apt-repository \
      "deb [arch=amd64] https://download.docker.com/linux/debian \
      $(lsb_release -cs) \
      stable" \
  && \
    add-apt-repository \
      "deb [arch=amd64] http://storage.googleapis.com/bazel-apt stable jdk1.8" \
  && \
    apt-get update \
  && \
    apt-get -y install \
      bazel \
      docker-ce \
  && \
    apt-get -y upgrade \
  && \
    mv /usr/bin/bazel /builder/bazel \
  && \
    mv /usr/bin/bazel-real /builder/bazel-real \
  && \
    mv /builder/bazel.sh /usr/bin/bazel

# Store the Bazel outputs under /workspace so that the symlinks under bazel-bin (et al) are accessible
# to downstream build steps.
RUN mkdir -p /workspace
RUN echo 'startup --output_base=/workspace/.bazel' > ~/.bazelrc

ENTRYPOINT ["bazel"]
