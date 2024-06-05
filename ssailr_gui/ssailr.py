import os
import subprocess
from PyQt5.QtWidgets import QWidget, QMessageBox

class SSAILR(QWidget):
    def __init__(self):
        super().__init__()

    def calculate(self, counts_type, output_dir, progress_bar):
        run_script = "python3 modified_counts.py"
        
        if not os.path.exists(output_dir):
            QMessageBox.critical(self, "Error", "Output directory doesn't exist.")
            return
        else:
            print(f"{output_dir} exists.")
            run_script += f" -dir {output_dir}"
        
        run_script += f" -count {counts_type}"
        
        print(run_script)
        try:
            progress = 0
            progress_bar.setValue(progress)
            res = subprocess.Popen(run_script.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            
            while True:
                output = res.stdout.readline()
                print(output)

                if res.poll() is not None:
                    break
                if output:
                    progress = min(progress + 1, 100)
                    progress_bar.setValue(progress)

            if res.returncode == 0:
                progress_bar.setValue(100)
                QMessageBox.information(self, "Success", "SSAILR completed successfully. Now wait while we generate graphs.")
            else:
                error_message = res.stderr.read()
                QMessageBox.critical(self, "Error", f"An error occurred: {error_message}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
    
    def generate_graphs(self, counts_type, output_dir):
        # Display input directory
        print(f"Current graph directory: {output_dir}.")

        # Generate histos
        for i in range(1, 4):
            run_script = f"python3 graphs.py {output_dir} {i}"
            print(run_script)

            try:
                res = subprocess.Popen(run_script.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

                while True:
                    output = res.stdout.readline()
                    print(output)
                    if res.poll() is not None:
                        break

                if res.returncode == 0:
                    if i == 3:
                        QMessageBox.information(self, "Success", "Graphs generated successfully.")
                else:
                    error_message = res.stderr.read()
                    QMessageBox.critical(self, "Error", f"An error occurred: {error_message}")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")