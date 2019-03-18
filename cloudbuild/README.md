# Builder image for GCB

This is based on the official gcr.io/cloud-builders/bazel, with some
modifications to support testing the LiME Frontend:
  * Switch base to Debian Buster Slim - provides Python 3.7
  * Add postgresql. Not actually used in tests, but required by PyGreSQL at
    install time.
