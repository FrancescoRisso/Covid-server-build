# Software requirement
```
pip3 install flask
sudo apt install gunicorn
git pull [...]
```

# Launch
```
gunicorn -b :[port] server:app
```
