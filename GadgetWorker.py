import random
import time
import logging
import coloredlogs
from tqdm import tqdm
import subprocess
import sys

# Configure colored logging
coloredlogs.install(level='DEBUG')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# List of available Python programs
scripts = [
    'GadgetGenerator.py',
    'GadgetIssueGenerator.py',
    'GadgetIssueCloser.py',
    'Gadget.py'
    # You can easily add more scripts here
]

# Minimum and maximum time in minutes
MIN_TIME = 15
MAX_TIME = 120


def run_script(script):
    """Runs the given script using a subprocess."""
    if script:
        logger.info(f"Running script: {script}")
        try:
            result = subprocess.run([sys.executable, script], check=True)
            logger.info(f"Successfully ran {script}")
            return result.returncode  # Return the exit code of the script
        except subprocess.CalledProcessError as e:
            logger.error(f"Error running {script}: {e}")
            return 2
    else:
        logger.info("No script selected to run.")
        return 0


def main():
    logger.info("Starting GadgetWorker...")

    try:
        last_exit_code = None
        while last_exit_code != 2:
            # If the time is between 0600 and 1800 EST, run the GadgetGenerator
            current_hour = time.localtime().tm_hour
            if 6 <= current_hour < 22:
                # Pick a random script or None
                script_to_run = random.choice(scripts + [None])
                logger.info(f"Selected script: {script_to_run if script_to_run else 'None'}")

                # Run the selected script or None
                last_exit_code = run_script(script_to_run)
            else:
                logger.info("Outside of the 6 AM - 10 PM window. No scripts will be run.")

            if last_exit_code is None or last_exit_code < 2:
                # Pick a random time between MIN_TIME and MAX_TIME in minutes
                delay_minutes = random.randint(MIN_TIME, MAX_TIME)
                delay_seconds = delay_minutes * 60
                logger.info(f"Waiting for {delay_minutes} minutes...")

                # Progress bar for the delay
                for _ in tqdm(range(delay_seconds), desc=f"Waiting {delay_minutes} minutes", unit="s"):
                    time.sleep(1)

    except KeyboardInterrupt:
        logger.info("GadgetWorker stopped by the user.")


if __name__ == "__main__":
    main()
