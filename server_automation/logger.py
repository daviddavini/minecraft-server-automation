from server_automation import utilities

import os
import datetime

LOGS_DIR = utilities.PACKAGE_PARENT_DIR / 'automation_logs'

BASE_LOG_FILENAME = 'automation.log'
STAMPED_LOG_FILENAME = 'automation' + '_' + utilities.date_stamp() + '.log'

# LOG_FLAGS_TO_PATHS = {
#   'update': LOGS_DIR / "update.log",
#   'control': LOGS_DIR / "control.log"
# }

# TODO: remove log_flag or replace with something better

def log(output, log_flag=None, format = None):
  '''Logs the output based on the given log flag.'''

  if format == 'title':
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    output = '\n--*-- {} --*-- ({})'.format(output, timestamp)
  
  elif format == 'header':
    output = '--- {} ---'.format(output)

  # Print the log into the terminal
  print(output)

  # Create the automation_logs dir, if it does not exist
  if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

  #IMPORTANT: Create the path down here, in case it didn't exist
  log_path = LOGS_DIR / STAMPED_LOG_FILENAME

  # Open the log file and write to it (TODO: Improve efficiency, by keeping resource open?)
  with open(log_path, "a+") as log_file:
    log_file.write(output + "\n")