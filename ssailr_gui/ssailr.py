import os
from PyQt5.QtWidgets import QWidget, QMessageBox, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal


class SSAILRWorkerThread(QThread):
    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(int)

    def __init__(self, method, *args):
        super().__init__()
        self.method = method
        self.args = args

    def run(self):
        try:
            self.method(*self.args)
            self.finished_signal.emit(0)
        except Exception as e:
            self.output_signal.emit(f"Error: {str(e)}")
            self.finished_signal.emit(1)

class SSAILR(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None

    def calculate(self, counts_type, output_dir, output_text: QTextEdit):
        run_script = "python3 modified_counts.py"
        
        if not os.path.exists(output_dir):
            QMessageBox.critical(self, "Error", "Output directory doesn't exist.")
            return
        else:
            print(f"{output_dir} exists.")
            run_script += f" -dir {output_dir}"
        
        run_script += f" -count {counts_type}"
        print(run_script)
        
        self.start_worker(run_script, output_text, self.on_calculate_finish)

    def on_calculate_finish(self, returncode):
        if returncode == 0:
            QMessageBox.information(self, "Success", "SSAILR completed successfully. Now wait while we perform the next step.")
        else:
            QMessageBox.critical(self, "Error", f"An error occurred. Please check the logs for more details.")

    def generate_graphs(self, output_dir, generate_scatter_plot, generate_histos, output_text: QTextEdit):
        print(f"Current graph directory: {output_dir}.")

        self.graph_tasks = []
        for i in range(1, 4):
            if not generate_scatter_plot and i == 1:
                continue
            if not generate_histos and (i == 2 or i == 3):
                continue
            
            run_script = f"python3 graphs.py {output_dir} {i}"
            print(run_script)

            self.graph_tasks.append((run_script, i))

        self.process_next_graph(output_text)

    def process_next_graph(self, output_text):
        if self.graph_tasks:
            run_script, graph_type = self.graph_tasks.pop(0)
            self.start_worker(run_script, output_text, lambda returncode: self.on_graph_finish(returncode, graph_type, output_text))
        else:
            QMessageBox.information(self, "Success", "Graphs generated successfully.")

    def on_graph_finish(self, returncode, graph_type, output_text):
        if returncode == 0:
            if graph_type == 3:
                QMessageBox.information(self, "Success", "Graphs generated successfully.")
        else:
            QMessageBox.critical(self, "Error", "An error occurred during graph generation. Please check the logs for more details.")
        self.process_next_graph(output_text)

    def start_worker(self, run_script, output_text, finish_callback):
        if self.worker is not None:
            self.worker.wait()

        self.worker = SSAILRWorkerThread(run_script)
        self.worker.output_signal.connect(output_text.append)
        self.worker.output_signal.connect(print)
        self.worker.finished_signal.connect(finish_callback)
        self.worker.start()