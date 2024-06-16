import schedule
import time
import subprocess
import logging

# Configure logging
logging.basicConfig(filename=r'C:\Users\malha\PycharmProjects\TechPal\logs\scheduler_log_file.log', level=logging.INFO, format='%(asctime)s %(message)s')

def job():
    logging.info('Job started')
    result = subprocess.run([r"C:\Users\malha\PycharmProjects\TechPal\.venv1\include\site\python3.11", r"C:\Users\malha\PycharmProjects\TechPal\scraping.py"])
    logging.info(f'Job finished with return code {result.returncode}')

# Schedule the job every 3 months
schedule.every(90).days.at('00:00').do(job)

logging.info('Scheduler started')
while True:
    schedule.run_pending()
    time.sleep(1)
