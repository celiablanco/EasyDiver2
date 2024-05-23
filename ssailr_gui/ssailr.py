import os
import subprocess
from PyQt5.QtWidgets import QWidget, QMessageBox

class SSAILR(QWidget):
    def __init__(self):
        super().__init__()

    def calculate(self, counts_type, output_dir):
        run_script = "python3 modified_counts.py"
        
        if not os.path.exists(output_dir):
            QMessageBox.critical(self, "Error", "Output directory doesn't exist.")
            return
        else:
            run_script += f" -dir {output_dir}"
        
        run_script += f" -count {counts_type}"
        
        print(run_script)
        try:
            res = subprocess.Popen(run_script.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            
            while True:
                output = res.stdout.readline()
                print(output)

                if res.poll() is not None:
                    break

            if res.returncode == 0:
                QMessageBox.information(self, "Success", "Task completed successfully.")
                self.close()
            else:
                error_message = res.stderr.read()
                QMessageBox.critical(self, "Error", f"An error occurred: {error_message}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
    
    def generate_histo_graphs(self, counts_type):
        # Check if figures directory exists
        output_dir = "figures"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Generate histos
        for i in range(1, 4):
            if i == 1:
                file_path = ""
            elif i == 2:
                file_path = "data/pipeline.output"
            else:    
                file_path = "data/pipeline.output"

            run_script = f"python3 graphs.py {file_path} {i}"

            try:
                subprocess.Popen(run_script.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")