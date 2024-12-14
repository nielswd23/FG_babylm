import time
import shutil
from datetime import datetime

"""
Tracking the grammars during FG training to see when it converges
"""

# Path to the file being updated
source_file = ("./fg-source-code-restore/out/brown_adam/" + 
               "brown_adam.0.FG-output.rank-1.txt")

# Directory to save backups
backup_dir = "./training_grammars"

# Interval between backups in seconds
backup_interval = 60  # Adjust as needed (e.g., every 60 seconds)

def backup_file():
    while True:
        # Create a timestamped backup filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"{backup_dir}/file_backup_{timestamp}.txt"

        # Copy the file
        try:
            shutil.copy(source_file, backup_file)
            print(f"Backup created: {backup_file}")
        except Exception as e:
            print(f"Error creating backup: {e}")

        # Wait before the next backup
        time.sleep(backup_interval)

# Run the backup process
backup_file()
