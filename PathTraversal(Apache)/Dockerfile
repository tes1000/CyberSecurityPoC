From debian:latest

run apt update

run apt install wget libpcre3-dev libapr1-dev libaprutil1-dev build-essential tar -y

WORKDIR /opt

run wget https://archive.apache.org/dist/httpd/httpd-2.4.50.tar.gz

run tar -xvzf httpd-2.4.50.tar.gz

run httpd-2.4.50/configure
run make httpd-2.4.50/.
run make install httpd-2.4.50/.

run echo 'ServerRoot "/usr/local/apache2"\nListen 80\nLoadModule authn_file_module modules/mod_authn_file.so\nLoadModule authn_core_module modules/mod_authn_core.so\nLoadModule authz_host_module modules/mod_authz_host.so\nLoadModule authz_groupfile_module modules/mod_authz_groupfile.so\nLoadModule authz_user_module modules/mod_authz_user.so\nLoadModule authz_core_module modules/mod_authz_core.so\nLoadModule access_compat_module modules/mod_access_compat.so\nLoadModule auth_basic_module modules/mod_auth_basic.so\nLoadModule reqtimeout_module modules/mod_reqtimeout.so\nLoadModule filter_module modules/mod_filter.so\nLoadModule mime_module modules/mod_mime.so\nLoadModule log_config_module modules/mod_log_config.so\nLoadModule env_module modules/mod_env.so\nLoadModule headers_module modules/mod_headers.so\nLoadModule setenvif_module modules/mod_setenvif.so\nLoadModule version_module modules/mod_version.so\nLoadModule unixd_module modules/mod_unixd.so\nLoadModule status_module modules/mod_status.so\nLoadModule autoindex_module modules/mod_autoindex.so\nLoadModule cgid_module modules/mod_cgid.so\nLoadModule dir_module modules/mod_dir.so\nLoadModule alias_module modules/mod_alias.so\n<IfModule unixd_module>\nUser daemon\nGroup daemon\n</IfModule>\nServerAdmin you@example.com\nDocumentRoot "/usr/local/apache2/htdocs"\n<IfModule dir_module>\nDirectoryIndex index.html\n</IfModule>\n<Files ".ht*">\n    Require all denied\n</Files>\nErrorLog "logs/error_log"\nLogLevel warn\n<IfModule log_config_module>\nLogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined\n    LogFormat "%h %l %u %t \"%r\" %>s %b" common\n    <IfModule logio_module>\nLogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" %I %O" combinedio\n</IfModule>\n    CustomLog "logs/access_log" common\n</IfModule>\n<IfModule alias_module>\nAlias /cgi-bin/ "/cgi-bin/"\n</IfModule>\n<IfModule cgid_module>\n</IfModule>\n<IfModule headers_module>\n    RequestHeader unset Proxy early\n</IfModule>\n<IfModule mime_module>\n    TypesConfig conf/mime.types\n    AddType application/x-compress .Z\n    AddType application/x-gzip .gz .tgz\n</IfModule>\n<IfModule proxy_html_module>\nInclude conf/extra/proxy-html.conf\n</IfModule>\n<IfModule ssl_module>\nSSLRandomSeed startup builtin\nSSLRandomSeed connect builtin\n</IfModule>' > /usr/local/apache2/conf/httpd.conf


#run sed -i 's@Options None@Options +ExecCGI@g' /usr/local/apache2/conf/httpd.conf

CMD ["/usr/local/apache2/bin/httpd", "-DFOREGROUND"]