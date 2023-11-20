FROM debian:latest

RUN apt update

RUN apt install wget libpcre3-dev libapr1-dev libaprutil1-dev build-essential tar -y

WORKDIR /opt

RUN wget https://archive.apache.org/dist/httpd/httpd-2.4.18.tar.gz

RUN wget https://ftp.gnu.org/gnu/bash/bash-4.0.tar.gz

RUN tar -xvzf httpd-2.4.18.tar.gz

RUN tar -xvzf bash-4.0.tar.gz

RUN httpd-2.4.18/configure
RUN make httpd-2.4.18/.
RUN make install httpd-2.4.18/.

RUN sed -i 's@#LoadModule cgid_module modules/mod_cgid.so@LoadModule cgid_module modules/mod_cgid.so@g' /usr/local/apache2/conf/httpd.conf

RUN sed -i 's@Options None@Options +ExecCGI@g' /usr/local/apache2/conf/httpd.conf

RUN echo '#!/usr/local/bin/bash\n# Set the content type to plain text\necho "Content-Type: text/plain"\n# Print a blank line to separate the headers from the content\necho ""\n\n# Log the User-Agent header to a file\necho "$HTTP_USER_AGENT > /usr/local/apache2/shellshock/customLogger.txt"\necho "Connected: $HTTP_USER_AGENT"' > /usr/local/apache2/cgi-bin/logger

RUN chmod +X /usr/local/apache2/cgi-bin/logger
RUN chmod 755 /usr/local/apache2/cgi-bin/logger

RUN bash-4.0/configure
RUN make bash-4.0/.
RUN make install bash-4.0/.


CMD ["/usr/local/apache2/bin/httpd", "-DFOREGROUND"]