from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor

class Worker:

	def __init__(self, logger, worker_count=2):
		self.logger = logger
		self.worker_count = worker_count
		self.quantity = 1
		self.job_id = 1
		self.link = None
	
	def work(self, n):
		self.logger.info('Current Job : %s' % n)

		if self.job_id == 100 :
			try:
				print('here comes conccurent task. You can call object here')
			except Exception as e:
				print(e)

		elif self.job_id == 101:
			try:
				print('for example call verifiy_email concurrently')
			except Exception as e:
				print(e)

		return True


	def start(self):
		
		total_works = self.quantity

		self.logger.info("Start work for %s quantity of %s with %s workers " % (self.link, total_works, self.worker_count))
		
		if (self.worker_count == 0):
			with ProcessPoolExecutor() as executor:
				for i in range(total_works):
					executor.submit(self.work, (i))

		else :
			with ThreadPoolExecutor(max_workers=self.worker_count) as executor:
				for i in range(total_works):
					executor.submit(self.work, i)

		return True

