#!/bin/bash

VAGRANT_HOST_DIR=/mnt/host_machine

########################
# Jenkins & Java
########################
echo "Installing Jenkins and Java"
wget -q -O - http://pkg.jenkins-ci.org/debian/jenkins-ci.org.key | sudo apt-key add -
sudo sh -c 'echo deb http://pkg.jenkins-ci.org/debian binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys FCEF32E745F2C3D5 > /dev/null 2>&1
sudo apt-get update > /dev/null 2>&1
sudo apt-get -y install default-jdk jenkins > /dev/null 2>&1
echo "Installing Jenkins default user and config"
sudo cp $VAGRANT_HOST_DIR/JenkinsConfig/config.xml /var/lib/jenkins/
sudo mkdir -p /var/lib/jenkins/users/admin
sudo cp $VAGRANT_HOST_DIR/JenkinsConfig/users/admin/config.xml /var/lib/jenkins/users/admin/
sudo chown -R jenkins:jenkins /var/lib/jenkins/users/
sudo sh -c 'echo "jenkins ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/jenkins'


########################
# Docker
########################
echo "Installing Docker"
sudo apt-get -y install docker.io
sudo systemctl enable docker
sudo usermod -aG docker ${USER}
sudo usermod -aG docker jenkins
sudo usermod -aG docker ubuntu
sudo usermod -aG docker vagrant

########################
# nginx
########################
echo "Installing nginx"
sudo apt-get -y install nginx > /dev/null 2>&1
sudo service nginx start

########################
# Configuring nginx
########################
echo "Configuring nginx"
cd /etc/nginx/sites-available
sudo rm -f default ../sites-enabled/default
sudo cp /mnt/host_machine/VirtualHost/jenkins /etc/nginx/sites-available/
sudo ln -sf /etc/nginx/sites-available/jenkins /etc/nginx/sites-enabled/
sudo service nginx restart
sudo service jenkins restart
echo "Success"

########################
# Misc tools
########################
echo "Installing tools"
sudo apt-get -y install redis-tools git htop build-essential autoconf automake libpcre3-dev libevent-dev pkg-config zlib1g-dev libssl-dev > /dev/null 2>&1
