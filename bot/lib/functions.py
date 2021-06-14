import signal,psutil
import os
import threading
import string, random


def generate_string(size=10, chars=None):
	if chars is None:
		chars = string.ascii_uppercase+string.ascii_lowercase+string.digits
	return (''.join(random.choice(chars) for _ in range(size)))


def generate_password(size=10, chars=None):
	"""
	if chars is None:
		chars = string.ascii_uppercase+string.ascii_lowercase+string.digits
	return (''.join(random.choice(chars) for _ in range(size)))
	"""

	minNumbers = 2
	minChars = 2
	minLetters = size-minNumbers-minChars

	dat = ''.join((random.choice(string.ascii_letters) for i in range(minLetters)))
	dat += ''.join((random.choice(string.digits) for i in range(minNumbers)))
	#dat += ''.join((random.choice(string.punctuation) for i in range(minChars)))

	str_var = list(dat)
	random.shuffle(str_var)
	return (''.join(str_var))



def kill_child_processes(parent_pid, sig=signal.SIGTERM):
	try:
		parent = psutil.Process(parent_pid)
	except psutil.NoSuchProcess:
		return

	children = parent.children(recursive=True)
	for process in children:
		#os.kill(process)
		sigmap = {signal.SIGINT: signal.CTRL_C_EVENT,signal.SIGBREAK: signal.CTRL_BREAK_EVENT}
		#process.send_signal(sig)
		#process.kill()
		kill(process.pid,signal.SIGINT)




def kill(pid, signum):
	sigmap = {signal.SIGINT: signal.CTRL_C_EVENT, signal.SIGBREAK: signal.CTRL_BREAK_EVENT}

	if signum in sigmap and pid == os.getpid():
		pid = 0
	thread = threading.current_thread()
	handler = signal.getsignal(signum)

	if (signum in sigmap and
			thread.name == 'MainThread' and
			callable(handler) and
			pid == 0):
		event = threading.Event()

		def handler_set_event(signum, frame):
			event.set()
			return handler(signum, frame)

		signal.signal(signum, handler_set_event)
		try:
			os.kill(pid, sigmap[signum])
			while not event.is_set():
				pass
		finally:
			signal.signal(signum, handler)
	else:
		os.kill(pid, sigmap.get(signum, signum))
