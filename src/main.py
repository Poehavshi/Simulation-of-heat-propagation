
import subprocess
if __name__ == "__main__":
    process = subprocess.Popen(["python", "main_r.py"])
    process1 = subprocess.Popen(["python", "main_t.py"])

    process.wait()
    process1.wait()

