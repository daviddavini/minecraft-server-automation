# Minecraft Server Automation

A handy python package to automate version updates and server reboots for your (vanilla) Minecraft server.

## Dependencies
You need the python package `requests` installed:
```python
pip install requests
```

You need the linux package `screen` installed:
```python
sudo apt-get install screen
```

Make sure your server jar is named `server.jar`, and is in the root of the `server` directory.
Make sure your world directory is named `world`, and is in the root of the `server` directory.

## Installation
Put the `server_automation` directory into the directory containing your `server` folder.

```bash
<parent directory>
├── server
│   ├── world
│   │   └── ...
│   └── server.jar
└── server_automation
    └── ...
```
