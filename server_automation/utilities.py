import os
import server_automation
import pathlib
import datetime

# Path to root directory of this package
PACKAGE_ROOT = pathlib.Path(server_automation.__file__).parent

# Path to the parent of server_automation and server.
PACKAGE_PARENT_DIR = PACKAGE_ROOT.parent

# Path to server root. Assumes that the parent of this python package is the server root
SERVER_DIRNAME = 'server'
SERVER_ROOT = PACKAGE_PARENT_DIR / SERVER_DIRNAME

# Filename of server.jar
SERVER_JAR_FILENAME = 'server.jar'
SERVER_JAR_PATH = SERVER_ROOT / SERVER_JAR_FILENAME

def chdir_to_server_root():
  '''Changes cwd to the root of the server, if cwd is not already the server root.'''
  is_cwd_server_root = os.getcwd() == SERVER_ROOT
  if not is_cwd_server_root:
    os.chdir(SERVER_ROOT)

# TODO: Move this to top, without circular import?
from server_automation import versions

def datetime_now_PTZ():
  # Subtract away the server time error to get PTZ timezone (TODO: Change to more general solution)
  return datetime.datetime.now() - datetime.timedelta(hours=7)

def date_stamp():
  '''Returns a date stamp string, to be used as a file suffix.'''
  now = datetime_now_PTZ()
  stamp = now.strftime("%Y-%m-%d")
  return stamp

def time_stamp():
  '''Returns a time stamp string, to be used as a file suffix.'''
  now = datetime_now_PTZ()
  stamp = now.strftime("%Y-%m-%d--%H-%M-%S")
  return stamp

def version_and_time_stamp():
  '''Returns a string, the version and time stamp, to be used as a UNIQUE file suffix.'''
  # Make the file suffix
  
  version_id = versions.get_current_version()
  stamp = '_' + version_id + '--' + time_stamp()
  return stamp