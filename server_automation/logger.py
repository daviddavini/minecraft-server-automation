from server_automation import utilities

import datetime

LOGS_DIR = utilities.PACKAGE_ROOT / 'logs'

BASE_LOG_FILENAME = 'automation.log'
BASE_LOG_PATH = LOGS_DIR / BASE_LOG_FILENAME

LOG_FLAGS_TO_PATHS = {
  'update': LOGS_DIR / "update.log",
  'control': LOGS_DIR / "control.log"
}

# TODO: remove log_flag or replace with something better

def log(output, log_flag=None, format = None):
  '''Logs the output based on the given log flag.'''

  if format == 'title':
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    output = '--*-- {} --*-- ({})'.format(output, timestamp)
  
  elif format == 'header':
    output = '--- {} ---'.format(output)

  #log_path = LOG_FLAGS_TO_PATHS[log_flag]

  print(output)
  with open(BASE_LOG_PATH, "a+") as log_file:
    log_file.write(output + "\n")