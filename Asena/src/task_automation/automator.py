import logging
import schedule
import time
from datetime import datetime

class TaskAutomator:
    def __init__(self):
        self.tasks = []
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def add_task(self, task):
        self.tasks.append(task)
        self.logger.info(f"Task '{task}' added.")

    def remove_task(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
            self.logger.info(f"Task '{task}' removed.")
        else:
            self.logger.warning(f"Task '{task}' not found.")

    def list_tasks(self):
        if not self.tasks:
            self.logger.info("No tasks available.")
        else:
            self.logger.info("Current tasks:")
            for task in self.tasks:
                self.logger.info(f"- {task}")

    def schedule_reminder(self, task, time_str):
        try:
            schedule_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            schedule.every().day.at(schedule_time.strftime("%H:%M:%S")).do(self.remind_task, task)
            self.logger.info(f"Reminder for task '{task}' set for {schedule_time}.")
        except ValueError as e:
            self.logger.error(f"Invalid time format: {e}")

    def remind_task(self, task):
        self.logger.info(f"Reminder: It's time to do the task '{task}'.")

    def automate_tasks(self):
        self.logger.info("Automating tasks...")
        for task in self.tasks:
            self.logger.info(f"Executing task: {task}")
            # Implement the logic to automate the task here

    def run_scheduler(self):
        self.logger.info("Starting the task scheduler...")
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    automator = TaskAutomator()
    automator.add_task("Task 1")
    automator.add_task("Task 2")
    automator.list_tasks()
    automator.schedule_reminder("Task 1", "2025-02-27 15:30:00")
    automator.automate_tasks()
    automator.run_scheduler()