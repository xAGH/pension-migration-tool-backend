import glob
import os
import time

import schedule

from app.jobs.move_files_job import move_files_job
from mock.migration_request import generate_csv

schedule.every().hour.at(":00").do(move_files_job)

while True:
    schedule.run_pending()
    time.sleep(1)


def delete_csv_files(directory):
    """Delete all CSV files in the specified directory."""
    csv_files = glob.glob(os.path.join(directory, "*.csv"))
    if not csv_files:
        print("No CSV files found.")
        return

    for file_path in csv_files:
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")


def gen_data():
    for i in range(100):
        filename = f"carga{i}"
        generate_csv(
            f"files/SolicitudesEntrantes/{filename}.csv",
            100,
        )


# delete_csv_files("./")
# gen_data()
move_files_job()
