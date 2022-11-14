#!/usr/bin/bash
echo "TAG=28" > .env

set -xe

# Greeting :
echo "Hello , Starting deploy script  . . ."

# Checking arguments :

machine=$1
if  [ $# != 1 ]; then
    echo "You should provide one argument:
               deploy.sh <test/prod> "
    exit 1
fi

if [ $machine != "test" ] && [ $machine != "prod" ]; then
            echo "The argument should be 'test' or 'prod'. "
            exit 1
fi

echo "This is $machine machine "


# Making dest. directory and copping files :
ssh ubuntu@$machine 'sudo mkdir -p /home/ubuntu/dockerCompose;sudo chmod 777 /home/ubuntu/dockerCompose'
scp  -o StrictHostKeyChecking=no .env ubuntu@$machine:/home/ubuntu/dockerCompose
scp  -o StrictHostKeyChecking=no docker-compose.yml ubuntu@$machine:/home/ubuntu/dockerCompose


#############################################
###   Running dockers on dest. machine :  ###
#############################################

ssh  ubuntu@$machine 'cd /home/ubuntu/dockerCompose;

  # Stopping running conteiners and cleaning machine from docker images :
  if [ $(docker ps -q|wc -l) -gt 0 ] ;
     then docker ps -q|xargs docker stop ;
     else  echo  "There is no runnig docker containers on this machine";
  fi
  docker system prune -af

  # Pullling docker images and running docker compose :
  IP="$(curl api.ipify.org)";
  sudo chmod 777 .env;
  echo "REACT_APP_BACK_END_IP=$IP " >> .env;
  sudo docker login;
  sudo docker-compose pull;
  docker-compose up --no-build -d;'


# If it is the test machine testing the wesite :
if [ $machine== "test" ];then
 sleep 10s
 if [ $(curl -Is  http://test:3000/  | head -1 |grep -c "200") == 0 ];
        then echo "ERROR : The 'Attendance' website does not available ";
        exit 1;
 fi
fi
