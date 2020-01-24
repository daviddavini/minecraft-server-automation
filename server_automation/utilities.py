import os
import server_automation
import pathlib

# Path to root directory of this package
PACKAGE_ROOT = pathlib.Path(server_automation.__file__).parent

# Path to server root. Assumes that the parent of this python package is the server root
SERVER_DIRNAME = 'server'
SERVER_ROOT = PACKAGE_ROOT.parent / SERVER_DIRNAME

# Filename of server.jar
SERVER_JAR_FILENAME = 'server.jar'
SERVER_JAR_PATH = SERVER_ROOT / SERVER_JAR_FILENAME

def chdir_to_server_root():
  '''Changes cwd to the root of the server, if cwd is not already the server root.'''
  is_cwd_server_root = os.getcwd() == SERVER_ROOT
  if not is_cwd_server_root:
    os.chdir(SERVER_ROOT)