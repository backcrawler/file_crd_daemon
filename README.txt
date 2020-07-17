Here are instruction for installing daemon on UNIX as well as api information and various extras

-----------------------------------------------------------------------------------------------------------------------
API:

For GET request:
curl -i -X GET http://hostname/api/<str:hash_name>/
where <hash_name> is required file hash, returns HTTP 404 if nothing found

For POST request:
curl -i -X POST -H "Content-Type:multipart/form-data" -F "f=@filepath" http://hostname/api/
where <filepath> is the path for your file, if instance already exists it's immediately returned to the front
with 201 code and JSON with "name" value, if not - it's created and the same result is returned. Files are saved
in the directory specified in setting.MEDIA_ROOT

For DELETE request:
curl -i -X DELETE http://hostname/api/<str:hash_name>/
where <hash_name> is required file hash, returns HTTP 404 if such instance doesn't exists, if it does - deletes
the file from drive and then the model instance

-----------------------------------------------------------------------------------------------------------------------
INSTALLATION (on Debian/Ubuntu):

Postgres Database shall be installed with:
sudo apt-get install postgresql postgresql-contrib

Enter /etc/postgresql/ for observing
Then all required dependencies: user, user password, DB name, DB URI shall be fulfilled,
settings.py and keys.json must correspond with them
Starting postgres:
sudo service postgresql reload

Then python is installed:
sudo apt-get update
sudo apt-get install build-essential libssl-dev libffi-dev python-dev
curl -O https://www.python.org/ftp/python/3.7.6/Python-3.7.6.tar.xz  #for 3.7.6
tar -xf Python-3.7.3.tar.xz
cd Python-3.7.3
./configure --enable-optimizations
make -j 8
sudo make altinstall
sudo apt-get install python3-pip
sudo apt-get install python3-venv

And venv for project is configured:
python3 -m venv env
. ./env/bin/activate
pip install -r requirements.txt
python manage.py migrate

-----------------------------------------------------------------------------------------------------------------------
NGINX configuration:

server {
	listen <PORT> default_server;
	listen [::]:<PORT> ipv6only=on default_server;
	root <ROOT>;
	index index.html index.htm index.nginx-debian.html;
	server_name <IP_OR_NAME>;
	location /static {
		alias <MYLOCATION>;
	}
	location /media {
        alias <MYLOCATION2>;
	}
	location / {
		include proxy_params;
		proxy_pass http://127.0.0.1:<GUNICORN_PORT>;
		proxy_set_header X-Forwarded-Host $server_name;
		proxy_set_header X-Real-Ip $remote_addr;
		add_header P3P 'CP="ALL DSP COR PSa PSDa OUR NOR ONL UNI COM NAV"';
		add_header Access-Control-Allow-Origin *;
	}
}
where:
<PORT> is the main port the application is supposed to work
<ROOT> is the root path for project's manage.py
<IP_OR_NAME> is the resource's name/ip
<MYLOCATION> and <MYLOCATION2> are paths for static files and media files, could be removed in this context
<GUNICORN_PORT> is the port gunicorn is serving, nginx is used as a proxy here

Create symbolic link in /etc/nginx/sites-enabled and add your user to www-data group, then start:
sudo ln –s /etc/nginx/sites-enabled/<filename> /etc/nginx/sites-available/<filename>
sudo service nginx restart

-----------------------------------------------------------------------------------------------------------------------
Gunicorn and daemon (through supervisor) configuration:

nano <ROOT>/gunicorn_config.py
#where <ROOT> is the project's root

inside:
command = '<ROOT>/env/bin/gunicorn'
pythonpath = '<ROOT>'
bind = '127.0.0.1:<GUNICORN_PORT>'
workers = <N_WORKERS>
user = <USERNAME>
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=<myproject>.settings'
#<USERNAME> is the required user's name
#<myproject> is project's name
#<N_WORKERS> = 2*n_cores + 1

Then:
nano <ROOT>/bin/start_gunicorn.py

inside:
#!/bin/bash
source <ROOT>/env/bin/activate
exec gunicorn  -c "<ROOT>/gunicorn_config.py" <myproject>.wsgi

Starting .sh script as daemon:
sudo nano /etc/supervisor/conf.d/<myproject>.conf

inside:
[program:gunicorn]
command=<ROOT>/bin/start_gunicorn.sh
user=<USERNAME>
directory=<ROOT>
process_name=%(program_name)s
numprocs=1
autostart=true
autorestart=true
redirect_stderr=true

After it is done:
sudo service supervisor restart

The web server will serve as a daemon, proxied with nginx