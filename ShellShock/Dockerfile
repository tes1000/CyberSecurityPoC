FROM debian:latest

RUN apt update

RUN apt install wget libpcre3-dev libapr1-dev libaprutil1-dev build-essential tar netcat-traditional -y

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

RUN echo '<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>Apache Shell Shock Demo</title>\n    <style>\n        /* Initially hide the hint */\n        .hint {\n            display: none;\n            color: blue;\n            cursor: pointer;\n            }\n    </style>\n</head>\n<body>\n    <h1>Apache Shell Shock Demo</h1>\n    <p>The server is using a vulnerable version of Bash (Bash 4.0).</p>\n\n    <!-- Button to toggle hint visibility -->\n    <button onclick="toggleHint()">Toggle Hint</button>\n\n    <!-- Hidden field with hint -->\n    <p id="hintText" class="hint">The /cgi-bin/logger script takes user agent into bash variable</p>\n\n    <script>\n        // Boolean variable to track hint visibility\n        var hintVisible = false;\n\n        // JavaScript function to toggle hint visibility\n        function toggleHint() {\n            var hintText = document.getElementById("hintText");\n            hintVisible = !hintVisible; // Toggle the boolean value\n            hintText.style.display = hintVisible ? "block" : "none";\n        }\n    </script>\n</body>\n</html>\n' > /usr/local/apache2/htdocs/index.html

RUN bash-4.0/configure
RUN make bash-4.0/.
RUN make install bash-4.0/.


CMD ["/usr/local/apache2/bin/httpd", "-DFOREGROUND"]