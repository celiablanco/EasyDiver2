import os
import subprocess
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QFileDialog, QPushButton, QMessageBox, QProgressBar, QTextEdit
from PyQt5.QtGui import QIcon, QPixmap

from directory_edit import ClickableDirectoryEdit
from ssailr import SSAILR

class EasyDiver(QWidget):
    def __init__(self):
        super().__init__()
        self.ssailr = SSAILR()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Easy Diver")
        layout = QVBoxLayout()

        # Required parameters
        required_label = QLabel("REQUIRED")
        layout.addWidget(required_label)

        # Option -i
        self.input_label = QLabel('Input Directory Path:')
        self.input_dir_edit = ClickableDirectoryEdit()
        self.input_dir_edit.clicked.connect(self.browse_input)
        input_tooltip_icon = QLabel()
        input_tooltip_icon.setPixmap(QPixmap('ssailr_gui/assets/question_icon.png').scaled(20, 20))
        input_tooltip_icon.setToolTip("Select the directory containing the input files.")
        
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_dir_edit)
        input_layout.addWidget(input_tooltip_icon)
        layout.addLayout(input_layout)

        # Optional parameters
        optional_label = QLabel("OPTIONAL")
        layout.addWidget(optional_label)

        # Option -o
        self.output_label = QLabel('Output Directory Filepath:')
        self.output_dir_edit = QLineEdit()
        output_tooltip_icon = QLabel()
        output_tooltip_icon.setPixmap(QPixmap('ssailr_gui/assets/question_icon.png').scaled(20, 20))
        output_tooltip_icon.setToolTip("Specify the directory to save output files. If not provided, it defaults to the input directory with '/pipeline.output' appended.")
        
        output_layout = QHBoxLayout()
        output_layout.addWidget(self.output_label)
        output_layout.addWidget(self.output_dir_edit)
        output_layout.addWidget(output_tooltip_icon)
        layout.addLayout(output_layout)

        # Option -p
        self.forward_primer_label = QLabel('Forward Primer Sequence Extraction:')
        self.forward_primer_edit = QLineEdit()
        forward_primer_tooltip_icon = QLabel()
        forward_primer_tooltip_icon.setPixmap(QPixmap('ssailr_gui/assets/question_icon.png').scaled(20, 20))
        forward_primer_tooltip_icon.setToolTip("Enter the forward primer sequence for extraction.")
        
        forward_primer_layout = QHBoxLayout()
        forward_primer_layout.addWidget(self.forward_primer_label)
        forward_primer_layout.addWidget(self.forward_primer_edit)
        forward_primer_layout.addWidget(forward_primer_tooltip_icon)
        layout.addLayout(forward_primer_layout)

        # Option -q
        self.reverse_primer_label = QLabel('Reverse Primer Sequence Extraction:')
        self.reverse_primer_edit = QLineEdit()
        reverse_primer_tooltip_icon = QLabel()
        reverse_primer_tooltip_icon.setPixmap(QPixmap('ssailr_gui/assets/question_icon.png').scaled(20, 20))
        reverse_primer_tooltip_icon.setToolTip("Enter the reverse primer sequence for extraction.")
        
        reverse_primer_layout = QHBoxLayout()
        reverse_primer_layout.addWidget(self.reverse_primer_label)
        reverse_primer_layout.addWidget(self.reverse_primer_edit)
        reverse_primer_layout.addWidget(reverse_primer_tooltip_icon)
        layout.addLayout(reverse_primer_layout)

        # Option -T
        self.threads_label = QLabel('Number of Threads:')
        self.threads_edit = QLineEdit()
        threads_tooltip_icon = QLabel()
        threads_tooltip_icon.setPixmap(QPixmap('ssailr_gui/assets/question_icon.png').scaled(20, 20))
        threads_tooltip_icon.setToolTip("Specify the number of threads to use for processing.")
        
        threads_layout = QHBoxLayout()
        threads_layout.addWidget(self.threads_label)
        threads_layout.addWidget(self.threads_edit)
        threads_layout.addWidget(threads_tooltip_icon)
        layout.addLayout(threads_layout)

        # Option -e
        self.extra_flags_label = QLabel('Extra Flags for PANDASeq (use quotes, e.g. "-L 50"):')
        self.extra_flags_edit = QLineEdit()
        extra_flags_tooltip_icon = QLabel()
        extra_flags_tooltip_icon.setPixmap(QPixmap('ssailr_gui/assets/question_icon.png').scaled(20, 20))
        extra_flags_tooltip_icon.setToolTip("Enter any extra flags for PANDASeq, enclosed in quotes (e.g., \"-L 50\").")
        
        extra_flags_layout = QHBoxLayout()
        extra_flags_layout.addWidget(self.extra_flags_label)
        extra_flags_layout.addWidget(self.extra_flags_edit)
        extra_flags_layout.addWidget(extra_flags_tooltip_icon)
        layout.addLayout(extra_flags_layout)
        
        # Option -a
        self.translate_check = QCheckBox('Translate to Amino Acids')
        translate_tooltip_icon = QLabel()
        translate_tooltip_icon.setPixmap(QPixmap('ssailr_gui/assets/question_icon.png').scaled(20, 20))
        translate_tooltip_icon.setToolTip("Check this box to translate nucleotide sequences to amino acids.")
        
        translate_layout = QHBoxLayout()
        translate_layout.addWidget(self.translate_check)
        translate_layout.addWidget(translate_tooltip_icon)
        layout.addLayout(translate_layout)

        # Option -r
        self.retain_check = QCheckBox('Retain Individual Lane Outputs')
        retain_tooltip_icon = QLabel()
        retain_tooltip_icon.setPixmap(QPixmap('ssailr_gui/assets/question_icon.png').scaled(20, 20))
        retain_tooltip_icon.setToolTip("Check this box to retain outputs for individual lanes.")
        
        retain_layout = QHBoxLayout()
        retain_layout.addWidget(self.retain_check)
        retain_layout.addWidget(retain_tooltip_icon)
        layout.addLayout(retain_layout)

        # Option for SSAILR
        self.run_ssailr = QCheckBox("Run Enrichment Analysis")
        ssailr_tooltip_icon = QLabel()
        ssailr_tooltip_icon.setPixmap(QPixmap('ssailr_gui/assets/question_icon.png').scaled(20, 20))
        ssailr_tooltip_icon.setToolTip("Check this box to run SSAILR for enrichment analysis.")
        
        ssailr_layout = QHBoxLayout()
        ssailr_layout.addWidget(self.run_ssailr)
        ssailr_layout.addWidget(ssailr_tooltip_icon)
        layout.addLayout(ssailr_layout)

        # Option for plots generation
        self.generate_plots = QCheckBox("Generate Plots")
        generate_plots_tooltip_icon = QLabel()
        generate_plots_tooltip_icon.setPixmap(QPixmap('ssailr_gui/assets/question_icon.png').scaled(20, 20))
        generate_plots_tooltip_icon.setToolTip("Check to generate plots from the data.")

        generate_plots_layout = QHBoxLayout()
        generate_plots_layout.addWidget(self.generate_plots)
        generate_plots_layout.addWidget(generate_plots_tooltip_icon)
        layout.addLayout(generate_plots_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # Horizontal layout
        button_layout = QHBoxLayout()

        # Cancel
        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.setToolTip("Click to cancel and close the application.")
        self.cancel_button.clicked.connect(self.close)
        button_layout.addWidget(self.cancel_button)

        # Submit
        submit_button = QPushButton("Submit", self)
        submit_button.setToolTip("Click to start the process with the specified parameters.")
        submit_button.clicked.connect(self.submit)
        button_layout.addWidget(submit_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)
        
    def browse_input(self):
        directory = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if directory:
            self.input_dir_edit.setText(directory)

    def submit(self):
        run_script = "bash easydiver.sh "
        if not self.input_dir_edit.text():
            QMessageBox.critical(self, "Error", "Please enter the required input.")
            return
        else:
            run_script += f"-i {self.input_dir_edit.text()}"
        
        if self.output_dir_edit.text():
            run_script += f" -o {self.output_dir_edit.text()}"
            output_dir = f"{self.input_dir_edit.text()}/{self.output_dir_edit.text()}"
        else:
            output_dir = f"{self.input_dir_edit.text()}/pipeline.output"

        if self.forward_primer_edit.text():
            run_script += f" -p {self.forward_primer_edit.text()}"

        if self.reverse_primer_edit.text():
            run_script += f" -q {self.reverse_primer_edit.text()}"

        if self.threads_edit.text():
            run_script += f" -T {self.threads_edit.text()}"

        if self.translate_check.isChecked():
            run_script += " -a"
            counts_type = "counts.aa"
        else:
            counts_type = "counts"

        if self.retain_check.isChecked():
            run_script += " -r"

        if self.extra_flags_edit.text():
            run_script += f" -e \"{self.extra_flags_edit.text()}\""

        print(run_script)
        self.progress_bar.setValue(0)

        # Execute the script
        try:
            progress = 0
            res = subprocess.Popen(run_script.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            
            while True:
                output = res.stdout.readline()
                print(output)
                if res.poll() is not None:
                    break

                self.progress_bar.setValue(progress)
                progress += 1

            if res.returncode == 0:
                self.progress_bar.setValue(100)
                QMessageBox.information(self, "Success", "EasyDiver completed successfully. Now wait while we calculate enrichment analysis.")

                # Run SSAILR
                if self.run_ssailr.isChecked():
                    self.ssailr.calculate(counts_type, output_dir, self.progress_bar)

                # Generate plots
                if self.generate_plots.isChecked():
                    generate_histos = True
                    if self.run_ssailr.isChecked():
                        generate_scatter_plot = True
                    else:
                        generate_scatter_plot = False
                else:
                    generate_histos = False               
                
                self.ssailr.generate_graphs(counts_type, output_dir, generate_scatter_plot, generate_histos)
                
                # Close EasyDiver + SSAILR Window
                self.close()
            else:
                error_message = res.stderr.read()
                QMessageBox.critical(self, "Error", f"An error occurred: {error_message}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")