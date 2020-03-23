import requests
import os
import hashlib
import subprocess
import json
import pathlib
import urllib
import shutil
import time
import datetime
import functools

from server_automation import utilities
from server_automation import logger
from server_automation import control

VERSION_MANIFEST_URL = "https://launchermeta.mojang.com/mc/game/version_manifest.json"

# The path to the backups directory
BACKUPS_DIRNAME = 'world_backups'
BACKUPS_DIR = utilities.SERVER_ROOT / BACKUPS_DIRNAME

# The path to the server's world directory
WORLD_DIRNAME = 'world'
WORLD_PATH = utilities.SERVER_ROOT / WORLD_DIRNAME

@functools.lru_cache()
def get_version_manifest():
  '''Load the version manifest json (from the internet).'''

  # Do a GET request for version manifest (from the interwebs)
  response = requests.get(url=VERSION_MANIFEST_URL)
  version_manifest = response.json()
  return version_manifest

@functools.lru_cache()
def get_latest_version(updateToSnapShot = False):
  '''Returns the latest version of minecraft.'''

  logger.log('Identifying the latest version of server.jar available...', 'update')

  if updateToSnapShot:
      latest_version = get_version_manifest()['latest']['snapshot']
  else:
      latest_version = get_version_manifest()['latest']['release']

  logger.log('Latest version is ' + latest_version + '.', 'update')

  return latest_version

@functools.lru_cache()
def get_current_version():
  '''Returns the current version of the server.'''

  logger.log('Identifying the current version of server.jar...', 'update')

  # If server.jar does not exist, return None
  if not os.path.exists(utilities.SERVER_JAR_PATH):
    logger.log('Cannot find server.jar.', 'update')
    return None

  # Unzip server.jar and look at version.json for the version number
  output = subprocess.check_output(['unzip', '-p', utilities.SERVER_JAR_PATH, 'version.json'])
  version_json = output.decode('UTF-8')
  version_dict = json.loads(version_json)
  current_version = version_dict['name']

  logger.log('Current version of server.jar is {}.'.format(current_version), 'update')
  return current_version

def download_server_jar(version_id = None):
  '''Download server.jar (from the interwebs).'''
  
  if version_id == None:
    version_id = get_latest_version()

  logger.log('Downloading version ' + version_id + ' of server.jar...', 'update')

  version = [version for version in get_version_manifest()['versions'] if version['id'] == version_id][0]
  jsonlink = version['url']
  response = requests.get(jsonlink)
  jardata = response.json()
  download_link = jardata['downloads']['server']['url']
  response = requests.get(download_link)
  with open(utilities.SERVER_JAR_PATH,'wb') as f:
    f.write(response.content)
  
  logger.log('Downloaded server.jar.', 'update')

def save_world_backup():
  '''Saves a backup of the server's world directory into the world_backups directory.'''

  logger.log('Saving a backup of ' + WORLD_DIRNAME + ' to ' +  BACKUPS_DIRNAME +  '...', 'update')

  # Create the world_backups dir, if it does not exist
  if not os.path.exists(BACKUPS_DIR):
    os.makedirs(BACKUPS_DIR)

  # Make the world backup dirname
  now = datetime.datetime.now()
  timestamp = now.strftime("%Y-%m-%d--%H-%M-%S")
  version_id = get_current_version()
  backup_dirname = WORLD_DIRNAME + '_' + version_id + '--' + timestamp
  backup_path = BACKUPS_DIR / backup_dirname

  # Copy the world directory into the backup directory
  shutil.copytree(WORLD_PATH, backup_path)

  logger.log('Backup saved.', 'update')

def update_check():
  '''Checks whether or not the server is running the latest version of server.jar, and updates server.jar if necessary.'''

  logger.log('Update Check', 'update', format='header')

  if get_latest_version() == get_current_version():
    logger.log('Server is already up to date.', 'update')
    return

  logger.log('Server is not up to date! Performing update now...', 'update')

  # Make sure we properly turn off the server, first of all
  control.stop_server()

  download_server_jar()
  logger.log('Server is now up to date.', 'update')

  # Now that we updated the server.jar, we should turn the server back on
  # TODO: Prevent two server_automation calls interfering with eachother
  control.start_server()

# TODO: Replace these params with global funcs that store a save