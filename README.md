# Software requirement
```
pip3 install flask
sudo apt install gunicorn
sudo apt install nginx
git pull [...]
```

# Set gunicorn
It is the web server that will serve the data (the api.js file)

We have to set it to automatically open, so we set it as a service

Create a new service file using  `sudo [yourTextEditor] /etc/systemd/system/[fileName].service`

Write the file using this template:
```
[Unit]
Description=Covid dashboard api
After=network.target

[Service]
User=[yourUbuntuUsername]
WorkingDirectory=[fullPathToTheWebserver]
ExecStart=gunicorn -b 127.0.0.1:[port] -w [n (see below)] api:app
Restart=always

[Install]
WantedBy=multi-user.target
```
n above is the number of workers (parallel processes): it is suggested to have a number of workers of 1 + 2*number of cores

Reload systemctl with `sudo systemctl daemon-reload`

Activate your process with `sudo systemctl start [fileName]`

If you have to modify the api.js, just remember to run `sudo systemctl reload [fileName]` to reload it

# Set nginx
It is the web server that will serve the static files (the React app)

All the configuration is in `/etc/nginx/`

You have all the available sites in `./sites-available/` and all the active sites in `./sites-enable`

If this is the first nginx config, you should delete "default" from this last folder: `sudo rm /etc/nginx/sites-enabled/default`

Create your nginx config file with `sudo [yourTextEditor] /etc/nginx/sites-available/[name].nginx`

Write the file using this template (step by step explanation later):
```
server {
	listen [theChosenPort];
	root /home/cvd/Covid-server-build/build;
	index index.html;
	
	location /api {
		include proxy_params;
		proxy_pass [linkToApiServer];
	}
	
	location /static {
		expires 1y;
		add_header Cache-Control "public";
	}
	
	location / {
		try_files $uri $uri/ /index.html;
		add_header Cache-Control "no-cache";
	}
}
```
Link the file you created to the `./sites-enable` folder using `sudo ln -s [fileInSites-available] [pathToSites-enable]/[name].nginx`
Reload the service with `sudo systemctl reload nginx`
