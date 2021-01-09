with open("api.py", "r") as f:
  server = f.read()

changes = [
  {
    "from": '##\n#   Disable default flask logger\n#\n\nlog = logging.getLogger("werkzeug")\nlog.setLevel(logging.ERROR)\n',
    "to": ""
  },
  {
    "from": 'print(f"Error: ',
    "to": 'app.logger.error(f"'
  },
  {
    "from": 'print(f"{get_date()} ',
    "to": 'app.logger.info(f"'
  },
  {
    "from": 'if __name__ == "__main__":\n    app.run(host="localhost", port=3001, debug=False)',
    "to": 'if __name__ != "__main__":\n    gunicorn_logger = logging.getLogger("gunicorn.error")\n    app.logger.handlers = gunicorn_logger.handlers\n    app.logger.setLevel(gunicorn_logger.level)'
  }
]

for change in changes:
  server = server.replace(change["from"], change["to"])

with open("api.py", "w") as f:
  f.write(server)

print("Done")