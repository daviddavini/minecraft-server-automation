from server_automation import logger
from server_automation import utilities

import datetime
import os
import time
import subprocess

SERVER_SCREEN = 'minecraft_server'

def is_server_running():
  '''Returns whether or not the server is running (by seeing if the screen is open).'''
  process = subprocess.Popen(['screen', '-ls'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  return str(process.stdout.read()).count(SERVER_SCREEN)

def restart_check():
  '''Checks whether or not the server is running, and starts it if necessary (using screen).'''

  logger.log('Restart Check', 'control', format='header')

  if is_server_running():
    logger.log('Server is currently running.', 'control')
    return

  logger.log('Server is down.', 'control')
  start_server()
  logger.log('Server is back up.', 'control')

def call_server_command(command):
  '''Calls a command on the server (using screen).'''
  logger.log('Called server command: ' + command, 'control')
  command = ['screen', '-S', SERVER_SCREEN, '-p', '0', '-X', "stuff", '\n' + command + '\n']
  subprocess.run(command)

def broadcast(message):
  '''Broadcast a message to the server (using say command).'''
  call_server_command("say " + message)

def broadcast_countdown(event, duration):
  '''Broadcast a countdown for a server event.'''
  #TODO: Move this to its own module

  logger.log('Broadcasting countdown for ' + event + ' across ' + str(duration) + ' seconds...', 'control')

  broadcast('ATTENTION: ' + event + ' will occur in ' + str(duration) + ' seconds.')

  time_to_event = duration
  while time_to_event > 0:
    broadcast(event + ' in ' + str(time_to_event) + ' seconds.')
    if time_to_event > 10:
      time.sleep(10)
      time_to_event -= 10
    else:
      time.sleep(1)
      time_to_event -= 1
    
  logger.log('Broadcasted countdown complete.', 'control')

def shutdown_server():
  '''Shutdown the server.'''

  logger.log('Stopping server...', 'control')

  # Stop the server
  call_server_command('stop')

  # Give the server 5 seconds to clean up properly
  time.sleep(5)

  logger.log('Stopped server.', 'control')

def stop_server():
  '''Broadcast a countdown and shutdown the server.'''
  broadcast_countdown('Shutdown', 60)
  shutdown_server()

  # In case something goes horribly wrong, we want to save a backup of the world file
  save_world_backup()

def start_server():
  '''Start the server, if it is not already running (in a separate screen).'''

  # Important! server.jar will run the server WHEREVER it is called!
  utilities.chdir_to_server_root()

  # Important! server.jar will run MULTIPLE TIMES otherwise!
  if is_server_running():
    logger.log('Server is already running.', 'control')
    return

  logger.log('Starting server on screen ' + SERVER_SCREEN + '...', 'control')

  command = ['screen', '-S', SERVER_SCREEN, '-d', '-m', 'java', '-Xmx5120M', '-Xms5120M', '-jar', utilities.SERVER_JAR_PATH, 'nogui']
  subprocess.run(command)

  logger.log('Started server.', 'control')

  # Broadcast the time the server was started
  timestamp = str(datetime.datetime.now())
  broadcast('Started server. Timestamp: ' + timestamp)