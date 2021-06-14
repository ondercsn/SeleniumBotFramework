from bot.lib.functions import *

class Tasks:
	db = None

	def __init__(self,db=None):
		if db is not None:
			self.db = db

	def updateTaskDB(self, task_id, removeIfDone=False):
		try:
			self.db.execQuery('UPDATE tasks SET done_amount = done_amount+1 WHERE task_id = %s ' % task_id)
			if removeIfDone:
				if self.quantityOfDoneTasks(task_id) >= self.quantityOfAllTasks(task_id):
					try:
						self.db.execQuery('DELETE FROM tasks WHERE task_id = %s' % task_id)
					except Exception as e:
						raise Exception('couldnt delete task from list : ',e)
						pass
			return True
		except:
			return False

	def quantityOfDoneTasks(self, task_id):
		try:
			dat = self.db.fetchOne("SELECT done_amount FROM tasks WHERE task_id=%s" % task_id)
			return dat['done_amount']
		except Exception as e:
			raise Exception('Error fetching data : ',e)


	def quantityOfAllTasks(self, task_id):
		try:
			dat = self.db.fetchOne("SELECT amount FROM tasks WHERE task_id=%s" % task_id)
			return dat['amount']
		except:
			return False

	def truncateTasks(self):
		try:
			self.db.execQuery('DELETE FROM tasks')
			self.db.execQuery('VACUUM')
			return True
		except:
			raise Exception('not truncated')


	def getDataFromTask(self,task_id,data):
		dat = self.db.fetchOne("SELECT %s as fetchData FROM tasks WHERE task_id=%s" % (data,task_id))
		return dat['fetchData']

	def getUrlOfTask(self,task_id):
		dat = self.db.fetchOne("SELECT link FROM tasks WHERE task_id=%s" % task_id)
		return dat['link']

	def deleteTask(self,task_id):
		self.db.execQuery('DELETE FROM tasks WHERE task_id=' % task_id)
		return True

	def getNextTask(self):
		taskData = self.db.fetchOne('SELECT * FROM tasks WHERE done_amount < amount ORDER BY task_id ASC LIMIT 1')
		return taskData