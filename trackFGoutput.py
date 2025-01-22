import time
import shutil
from datetime import datetime

"""
Tracking the grammars during FG training to see when it converges.
"""

def readLastLine(my_file): 
    with open(my_file, "r") as file:
        file.seek(0, 2)  # Move the cursor to the end of the file
        position = file.tell()  # Get the position of the last byte
        line = ""
        while position >= 0:
            file.seek(position)  # Move to the current position
            char = file.read(1)  # Read one character
            if char == "\n" and line:  # Stop if a newline is found and there's content in `line`
                break
            line = char + line  # Prepend the character to `line`
            position -= 1

    return line.rstrip()


# Path to the file being updated
source_file = ("./fg-source-code-restore/out/brown_adam/" + 
               "brown_adam.0.FG-output.rank-1.txt")

debug_file = ("./fg-source-code-restore/out/brown_adam/" + 
              "brown_adam.0.FG-output-debug.txt")

# Interval between backups in seconds
backup_interval = 10*60


def track_grammar():
    prev_sweep_num = None
    while True:
        # timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # current grammar probability 
        with open(source_file, 'r') as file:
            prob_line = file.readline().rstrip()

        # sweep number 
        sweep_line = readLastLine(debug_file)

        # add info to a file 
        with open("FG_run_tracker.txt", 'a') as file:
            file.write(f"{timestamp}\n")
            file.write(f"Logprob: {prob_line}\n")
            file.write(f"{sweep_line}\n\n")

        # break when sweep number has not changed 
        sweep_num = int(sweep_line.split()[-1][:-1])
        if prev_sweep_num is not None: 
            if prev_sweep_num == sweep_num:
                break

        prev_sweep_num = sweep_num

        # Wait before the next backup
        time.sleep(backup_interval)

# Run the backup process
track_grammar()







#### OLD code to copy the entire grammar ####
# """
# Tracking the grammars during FG training to see when it converges.
# """

# # Path to the file being updated
# source_file = ("./fg-source-code-restore/out/brown_adam/" + 
#                "brown_adam.0.FG-output.rank-1.txt")

# debug_file = ("./fg-source-code-restore/out/brown_adam/" + 
#               "brown_adam.0.FG-output-debug.txt")

# # Directory to save backups
# backup_dir = "./training_grammars"

# # Interval between backups in seconds
# backup_interval = 10*60  

# def backup_file():
#     while True:
#         # Create a timestamped backup filename
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         backup_file = f"{backup_dir}/file_backup_{timestamp}.txt"

#         # Copy the file
#         try:
#             shutil.copy(source_file, backup_file)
#             print(f"Backup created: {backup_file}")
#         except Exception as e:
#             print(f"Error creating backup: {e}")

#         # Wait before the next backup
#         time.sleep(backup_interval)

# # Run the backup process
# backup_file()