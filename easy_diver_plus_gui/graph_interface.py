import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QFileDialog, QSplitter
from PyQt5.QtGui import QDoubleValidator, QIntValidator, QPixmap, QCloseEvent
from PyQt5.QtCore import Qt, QEvent # type: ignore # pylint: disable=import-error
from directory_edit import ClickableDirectoryEdit
from graphs_generator import main as gg_main

class Graphs_Window(QWidget):
    def __init__(self, parent = None, rounds_path = None):
        super().__init__(parent)
        if parent.__class__.__name__ == 'MainApp':
            parent.close()
            super().__init__()
        else:
            super().__init__(parent)
        self.rounds_path = rounds_path
        self.inputs = {}
        self.worker = None
        self.graph_tasks = []
        self.initUI()

    def initUI(self):
        # Create a splitter
        splitter = QSplitter(Qt.Vertical)
        layout = QVBoxLayout()
        self.required_widget = QWidget()
        self.required_layout = QVBoxLayout()
        self.required_label = QLabel("REQUIRED")
        self.required_layout.addWidget(self.required_label)
        if self.rounds_path is None:
            self.input_layout = QHBoxLayout()
            self.input_label = QLabel("Input Path for Parent Directory:")
            self.input_dir_edit = ClickableDirectoryEdit()
            self.input_dir_edit.clicked.connect(self.browse_input)
            self.input_tooltip_icon = QLabel()
            self.input_tooltip_icon.setPixmap(
                QPixmap("easy_diver_plus_gui/assets/question_icon.png").scaled(20, 20)
            )
            self.input_tooltip_icon.setToolTip(
                "Select the directory containing the analysis_output_nt folder. (e.g. pipeline_output)"
            )
            self.input_layout.addWidget(self.input_label)
            self.input_layout.addWidget(self.input_dir_edit)
            self.input_layout.addWidget(self.input_tooltip_icon)
            self.required_layout.addLayout(self.input_layout)
        # Select Round
        self.dna_or_aa_layout = QHBoxLayout()
        self.dna_or_aa_label = QLabel("Select Data Type:")
        self.dna_or_aa_combo = QComboBox()
        self.dna_or_aa_combo.addItem('DNA')
        self.dna_or_aa_combo.addItem('AA')
        self.dna_or_aa_combo.setCurrentIndex(-1)
        self.dna_or_aa_layout.addWidget(self.dna_or_aa_label)
        self.dna_or_aa_layout.addWidget(self.dna_or_aa_combo)
        self.dna_or_aa_combo.currentIndexChanged.connect(self.populate_rounds)
        self.required_layout.addLayout(self.dna_or_aa_layout)

        # Select Round
        round_layout = QHBoxLayout()
        round_label = QLabel("Select Round:")
        self.round_combo = QComboBox()
        self.populate_rounds()
        round_layout.addWidget(round_label)
        round_layout.addWidget(self.round_combo)
        self.required_layout.addLayout(round_layout)
        self.required_widget.setLayout(self.required_layout)
        splitter.addWidget(self.required_widget)

        # Define input configurations
        input_configurations = [
            ("Count_post", 0, 10000000, False),
            ("Freq_post", 0.0000000, 10000000.0000000, True),
            ("Count_pre", 0, 10000000, False),
            ("Freq_pre", 0.0000000, 10000000.0000000, True),
            ("Count_neg", 0, 10000000, False),
            ("Freq_neg", 0.0000000, 10000000.0000000, True),
            ("Enr_post", 0, 10000000, False),
            ("Enr_neg", 0, 10000000, False)
        ]
        self.optional_widget = QWidget()
        self.optional_layout = QVBoxLayout()

        optional_label = QLabel("OPTIONAL")
        self.optional_layout.addWidget(optional_label)

        for label_text, min_default, max_default, is_float in input_configurations:
            input_field_min, input_field_max = self.create_input_field(
                label_text, min_default, max_default, self.optional_layout, is_float)
            self.inputs[label_text] = input_field_min, input_field_max
        self.optional_widget.setLayout(self.optional_layout)
        splitter.addWidget(self.optional_widget)
        self.buttons_box = QHBoxLayout()
        
        layout.addWidget(splitter)
        # Generate Graphs Button
        self.generate_button = QPushButton("Generate Graphs")
        self.generate_button.clicked.connect(self.generate_graphs)
        self.buttons_box.addWidget(self.generate_button)

        # Generate Graphs Button
        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)
        self.buttons_box.addWidget(self.exit_button)
        layout.addLayout(self.buttons_box)

        self.setLayout(layout)
        self.setWindowTitle("Graph Generator")
        self.setWindowFlags(Qt.Window | Qt.Dialog)
        self.show()
        self.center_window()
    
    def populate_rounds(self):
        # Assuming the directory containing rounds is pre-defined in the code
        self.round_combo.clear()
        analysis_output = 'analysis_output'
        if self.dna_or_aa_combo.currentText() == 'AA':
            analysis_output = analysis_output+'_aa'
        else:
            analysis_output = analysis_output+'_nt'
        try:
            if self.rounds_path is not None:
                rounds_directory = f"{self.rounds_path}/{analysis_output}"
                rounds = sorted([f for f in os.listdir(rounds_directory) if f.startswith('round_')])
                for round_name in rounds:
                    self.round_combo.addItem(round_name.split('_')[1])
        except Exception as error:
            QMessageBox.critical(self, "Error", f"An error occurred:\n{error}")
            self.close()
    def create_input_field(self, label_text, min_default_value, max_default_value, layout, is_float=False):
        input_layout = QHBoxLayout()
        label = QLabel(label_text + " minimum & maximum:")
        input_field_min = QLineEdit()
        input_field_min.setText(str(min_default_value))
        input_field_max = QLineEdit()
        input_field_max.setText(str(max_default_value))
        if is_float:
            input_field_min.setValidator(QDoubleValidator(0.0, 1.0, 7))
            input_field_max.setValidator(QDoubleValidator(0.0, 1.0, 7))
        else:
            input_field_min.setValidator(QIntValidator(0, 10000))
            input_field_max.setValidator(QIntValidator(0, 10000))
        input_layout.addWidget(label)
        input_layout.addWidget(input_field_min)
        input_layout.addWidget(input_field_max)
        layout.addLayout(input_layout)
        return input_field_min, input_field_max

    def generate_graphs(self):
        # Implement the graph generation logic here
        analysis_output = 'analysis_output'
        if self.dna_or_aa_combo.currentText() == 'AA':
            analysis_output = analysis_output+'_aa'
        else:
            analysis_output = analysis_output+'_nt'
        input_values = {label: (vals[0].text(), vals[1].text()) for label, vals in self.inputs.items()}
        rounds_file = f"{self.rounds_path}/{analysis_output}/round_{self.round_combo.currentText()}_enrichment_analysis.csv"
        try:
            grapher = gg_main(rounds_file, input_values)
            if grapher is True:
                QMessageBox.information(self, "Graphs Generated", "The graphs have been generated successfully.")
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode('utf-8') if e.stderr else str(e)
            print("An error occurred:", error_msg)
            QMessageBox.critical(self, "Error", f"An error occurred:\n{error_msg}")

    def browse_input(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        analysis_output_exists = False
        if directory:
            for f in os.listdir(directory):
                if f == 'analysis_output_nt':
                    analysis_output_exists = True
                    self.input_dir_edit.setText(directory)
                    self.rounds_path = directory

        if analysis_output_exists is False:
            QMessageBox.critical(
                self,
                "Error",
                "Please choose the parent directory containing the 'analysis_output_nt' folder.",
            )

    def center_window(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def closeEvent(self, event: QCloseEvent) -> None: # pylint: disable=invalid-name
        """
        Handle the event when the application window is closed,
        ensuring the interaction button is disabled in the main window
        and the submit button is enabled in the main window, if and only if
        the saved choices was successful, meaning the sorting is completed.
        """
        # Ensure the parent exists and the button exists before trying to disable it
        if (self.parent() is not None):
            self.parent().close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Graphs_Window(parent = None, rounds_path = None)
    sys.exit(app.exec_())
