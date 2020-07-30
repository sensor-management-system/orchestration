#!/bin/bash

# Make sure you are in the gfz network (locally or via vpn)
# so that those servers are available
# export SMS_BACKEND_URL="http://rz-vm64.gfz-potsdam.de:5000"
# export CV_BACKEND_URL="http://rz-vm64.gfz-potsdam.de:5001"
# --> those variables are now inside of the docker-compose file
docker-compose -f docker-compose-gfz-local-with-staging-vm.yml up
