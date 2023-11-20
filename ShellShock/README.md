# ShellShock Test Lab

This lab is designed to underscore the significance of maintaining up-to-date software components and the risks associated with invalidated input. Specifically, it explores the Shellshock vulnerability, a critical security flaw that can lead to remote code execution in the widely used Bash shell. By emphasizing the importance of promptly updating and securing components, this lab serves as a practical demonstration of the potential consequences that can arise from overlooking the need for timely maintenance and validation of system inputs.

## Docker instructions
# download repo
git clone https://github.com/tes1000/CyberSecurityPoC.git

# build docker image
docker build . -t shellShock_Poc

# run container
docker run -p 80:80 shellShock_Poc

### Local Installation -> WARNING this lab is vulnerable to remote code execution, so only create within a controlled environment.

## Prerequisites

- Unix(These instructions are specifically for a debian distro)
- Basic command-line proficiency

## Installation Steps (as root)
# update system
apt update

# install dependencies
apt install wget libpcre3-dev libapr1-dev libaprutil1-dev build-essential tar netcat-traditional -y

# download vulnerable apache source files
wget https://archive.apache.org/dist/httpd/httpd-2.4.18.tar.gz

# download vulnerable bash source files
wget https://ftp.gnu.org/gnu/bash/bash-4.0.tar.gz

# unzip apache
tar -xvzf httpd-2.4.18.tar.gz

# unzip bash
tar -xvzf bash-4.0.tar.gz

# configure apache 
httpd-2.4.18/configure

# make apache binary
make httpd-2.4.18/.

# install apache binary
make install httpd-2.4.18/.

# enable neccisary modules
run sed -i 's@#LoadModule cgid_module modules/mod_cgid.so@LoadModule cgid_module modules/mod_cgid.so@g' /usr/local/apache2/conf/httpd.conf

# set vulnerable configuration
run sed -i 's@Options None@Options +ExecCGI@g' /usr/local/apache2/conf/httpd.conf

# create a cgi script that sets a user input into a bash variable
echo '#!/usr/local/bin/bash\n# Set the content type to plain text\necho "Content-Type: text/plain"\n# Print a blank line to separate the headers from the content\necho ""\n\n# Log the User-Agent header to a file\necho "$HTTP_USER_AGENT > /usr/local/apache2/shellshock/customLogger.txt"\necho "Connected: $HTTP_USER_AGENT"' > /usr/local/apache2/cgi-bin/logger

# make custom cgi script executable
chmod +X /usr/local/apache2/cgi-bin/logger

# set permissions
chmod 755 /usr/local/apache2/cgi-bin/logger

# configure bash
bash-4.0/configure

# make bash binary
make bash-4.0/.

# install bash binary
make install bash-4.0/.

# OPTIONAL HINT TEXT: Copy index html page to path /usr/local/apache2/htdocs/index.html

# start vulnerable service
service httpd start