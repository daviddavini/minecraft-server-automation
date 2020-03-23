from server_automation import logger
from server_automation import utilities
from server_automation import versions
from server_automation import control

import sys

if len(sys.argv) >= 2:

  if sys.argv[1] == '--update-check':
    versions.update_check()

  if sys.argv[1] == '--start-check':
    control.start_check()

  if sys.argv[1] == '--restart':
    control.restart()

else:
  versions.update_check()
  control.start_check()