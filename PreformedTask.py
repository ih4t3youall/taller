import datetime

class PreformedTask:

    def __init__(self, preformedTask):
        self.preformed_tasks = preformedTask
        self.task_date = datetime.date.today().strftime("%d-%m-%Y")

