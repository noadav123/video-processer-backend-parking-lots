import multiprocessing
import subprocess
import sys
from config import PARKING_CONFIGS
from parking_detector import run_detector

def run_api_server():
    import RestAPIServer

def main():
    processes = []

    for name, config in PARKING_CONFIGS.items():
        process = multiprocessing.Process(
            target=run_detector,
            args=(name, config),
            name=f"Detector-{name}"
        )
        process.start()
        processes.append(process)
    api_process = multiprocessing.Process(
        target=run_api_server,
        name="API-Server"
    )
    api_process.start()
    processes.append(api_process)

    try:
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        for process in processes:
            process.terminate()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()

