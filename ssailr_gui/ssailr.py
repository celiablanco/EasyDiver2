import os
import subprocess
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal

class WorkerThread(QThread):
    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(int)

    def __init__(self, run_script):
        super().__init__()
        self.run_script = run_script

    def run(self):
        res = subprocess.Popen(self.run_script.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
        while True:
            output = res.stdout.readline()
            if output:
                self.output_signal.emit(output.strip())

            if res.poll() is not None:
                break

        if res.returncode != 0:
            error_message = res.stderr.read()
            self.output_signal.emit(f"Error: {error_message.strip()}")
        self.finished_signal.emit(res.returncode)

class SSAILR(QWidget):
    def __init__(self):
        super().__init__()

    def calculate(self, counts_type, output_dir, output_text):
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
            self.worker = WorkerThread(run_script)
            self.worker.output_signal.connect(output_text.append)
            self.worker.output_signal.connect(print)
            self.worker.start()

            self.worker.finished.connect(lambda: self.on_finish(self.worker.returncode))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def on_finish(self, returncode):
        if returncode == 0:
            QMessageBox.information(self, "Success", "SSAILR completed successfully. Now wait while we perform the next step.")
        else:
            QMessageBox.critical(self, "Error", f"An error occurred. Please check the logs for more details.")
    
    def generate_graphs(self, output_dir, generate_scatter_plot, generate_histos, output_text):
        print(f"Current graph directory: {output_dir}.")

        for i in range(1, 4):
            if not generate_scatter_plot and i == 1:
                continue
            if not generate_histos and (i == 2 or i == 3):
                continue
            
            run_script = f"python3 graphs.py {output_dir} {i}"
            print(run_script)

            try:
                self.worker = WorkerThread(run_script)
                self.worker.output_signal.connect(output_text.append)
                self.worker.output_signal.connect(print)
                self.worker.start()

                self.worker.finished_signal.connect(lambda: self.on_graph_finish(self.worker.returncode, i))

            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def on_graph_finish(self, returncode, graph_type):
        if returncode == 0:
            if graph_type == 3:
                QMessageBox.information(self, "Success", "Graphs generated successfully.")
        else:
            QMessageBox.critical(self, "Error", "An error occurred during graph generation. Please check the logs for more details.")