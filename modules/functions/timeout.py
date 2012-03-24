class TimeoutException(Exception): 
  pass

def timeout_handler(signum, frame):
  raise TimeoutException()

def set_timeout(secs):
  import signal
  
  signal.signal(signal.SIGALRM, timeout_handler)
  signal.alarm(secs)