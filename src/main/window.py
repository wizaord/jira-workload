import logging
import sys
import traceback

from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout,
                             QWidget, QPushButton, QPlainTextEdit, QHBoxLayout,
                             QComboBox, QMessageBox)

# Import the modules containing the functions to call.
import workload_extract
import workload_extract_for_user
import workload_extract_for_user_and_technical_story


class LogSignaler(QObject):
    """Classe pour émettre des signaux de log de façon thread-safe"""
    log_signal = pyqtSignal(str)

class LogHandler(logging.Handler):
    def __init__(self, signaler):
        super().__init__()
        self.signaler = signaler

    def emit(self, record):
        msg = self.format(record)
        # Utilisation du signal pour envoyer le message de façon thread-safe
        self.signaler.log_signal.emit(msg)

def setup_logging(log_widget, signaler):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Niveau par défaut INFO
    
    # Clear existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()
        
    # Handler pour le widget
    handler = LogHandler(signaler)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Handler pour la console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

class WorkerThread(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, function):
        super().__init__()
        self.function = function
        self.running = True
    
    def run(self):
        try:
            self.function()
        except Exception as e:
            error_msg = f"Une erreur s'est produite: {str(e)}\n{traceback.format_exc()}"
            logging.error(error_msg)
            self.error.emit(error_msg)
        finally:
            self.running = False
            self.finished.emit()
    
    def stop(self):
        self.running = False
        # Attendre que le thread se termine naturellement
        self.wait(500)  # Attendre 500ms maximum

class JiraChachouExporter(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialisation du signaleur de logs
        self.log_signaler = LogSignaler()
        self.log_signaler.log_signal.connect(self.append_log)
        
        self.initUI()
        self.current_thread = None
        self.threads = []  # Pour garder une référence aux threads terminés
        
    def initUI(self):
        self.setWindowTitle("Jira Chachou Exporter")
        self.setMinimumSize(800, 500)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        label = QLabel("Jira Chachou Exporter")
        font = QFont("ITC Benguiat", 24, QFont.Bold)
        label.setFont(font)
        label.setStyleSheet("color: #ff6ec7; background-color: black; border: 3px solid #ff6ec7; padding: 10px;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        
        # Buttons
        btn1 = QPushButton("Lancer workload_extract")
        btn1.clicked.connect(lambda: self.run_in_thread(workload_extract.main))
        layout.addWidget(btn1)
        
        btn2 = QPushButton("Lancer workload_extract_for_user")
        btn2.clicked.connect(lambda: self.run_in_thread(workload_extract_for_user.main))
        layout.addWidget(btn2)
        
        btn3 = QPushButton("Lancer workload_extract_for_user_and_technical_story")
        btn3.clicked.connect(lambda: self.run_in_thread(workload_extract_for_user_and_technical_story.main))
        layout.addWidget(btn3)
        
        # --- Suppression du bouton Stop ---
        # self.btn_stop = QPushButton("Stop")
        # self.btn_stop.clicked.connect(self.stop_current_thread)
        # self.btn_stop.setEnabled(False)  # Désactivé par défaut
        # layout.addWidget(self.btn_stop)
        
        # Create a text area to display logs
        self.log_view = QPlainTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setMinimumHeight(200)
        
        # Création d'un layout horizontal pour la zone de logs et le bouton de purge
        log_layout = QHBoxLayout()
        
        # Création d'un layout vertical pour contenir le log_view et potentiellement d'autres contrôles
        log_container = QVBoxLayout()
        log_container.addWidget(self.log_view)
        
        # Ajout du sélecteur de niveau de log
        log_level_layout = QHBoxLayout()
        log_level_label = QLabel("Niveau de log:")
        self.log_level_combo = QComboBox()
        log_levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
        }
        for level_name in log_levels:
            self.log_level_combo.addItem(level_name)
        
        # Sélectionner INFO par défaut
        default_level_index = self.log_level_combo.findText("INFO")
        if default_level_index >= 0:
            self.log_level_combo.setCurrentIndex(default_level_index)
        
        self.log_level_combo.currentTextChanged.connect(self.change_log_level)
        
        log_level_layout.addWidget(log_level_label)
        log_level_layout.addWidget(self.log_level_combo)
        log_level_layout.addStretch(1)
        
        # Création d'un bouton pour purger les logs
        clear_log_btn = QPushButton("Purger les logs")
        clear_log_btn.setFixedWidth(100)
        clear_log_btn.clicked.connect(self.clear_logs)
        log_level_layout.addWidget(clear_log_btn)
        
        # Ajout du layout de niveau de log au conteneur de logs
        log_container.addLayout(log_level_layout)
        
        # Ajout des widgets au layout horizontal
        log_layout.addLayout(log_container, 1)  # Le log_container prend tout l'espace disponible
        
        # Ajout du layout horizontal au layout principal
        layout.addLayout(log_layout, 1)
        
        # La zone de logs s'étendra quand la fenêtre est redimensionnée
        layout.setStretchFactor(log_layout, 1)
        
        # Setup logging to display in the log_view.
        self.logger = setup_logging(self.log_view, self.log_signaler)
        self.change_log_level(self.log_level_combo.currentText())  # Appliquer le niveau de log initial
        logging.info("Log system initialized.")
        logging.info("La fenêtre peut maintenant être redimensionnée.")
    
    def append_log(self, message):
        """Méthode thread-safe pour ajouter un message au log"""
        self.log_view.appendPlainText(message)
        self.log_view.ensureCursorVisible()
    
    def change_log_level(self, level_name):
        log_levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
        }
        
        if level_name in log_levels:
            level = log_levels[level_name]
            logging.getLogger().setLevel(level)
            logging.info(f"Niveau de log changé à: {level_name}")
    
    def run_in_thread(self, function):
        # Empêcher le démarrage d'un nouveau thread si un thread est déjà en cours
        if self.current_thread and self.current_thread.isRunning():
            logging.warning("Une opération est déjà en cours. Attendez qu'elle soit terminée.")
            return
            
        # Désactiver les boutons pendant l'exécution
        for btn in self.findChildren(QPushButton):
            btn.setEnabled(False)
        
        # self.btn_stop.setEnabled(True)  # Activer le bouton Stop
        
        # Nettoyer les threads terminés
        self._cleanup_finished_threads()
        
        # Créer et démarrer le thread
        logging.info(f"Démarrage de {function.__module__}.{function.__name__}")
        self.current_thread = WorkerThread(function)
        self.current_thread.finished.connect(self.on_thread_finished)
        self.current_thread.error.connect(self.on_thread_error)
        self.threads.append(self.current_thread)  # Conserver une référence
        self.current_thread.start()
    
    def _cleanup_finished_threads(self):
        """Nettoyer les threads terminés pour libérer les ressources"""
        self.threads = [t for t in self.threads if t.isRunning()]
    
    def on_thread_finished(self):
        # Réactiver les boutons à la fin de l'exécution
        for btn in self.findChildren(QPushButton):
            btn.setEnabled(True)
        
        logging.info("Opération terminée.")
    
    def on_thread_error(self, error_msg):
        # En cas d'erreur, afficher un message
        QMessageBox.critical(self, "Erreur", error_msg)
    
    def stop_current_thread(self):
        if self.current_thread and self.current_thread.isRunning():
            logging.info("Arrêt du traitement en cours...")
            self.current_thread.stop()
    
    def clear_logs(self):
        self.log_view.clear()
        logging.info("Logs purgés.")
    
    def closeEvent(self, event):
        """Nettoyer proprement les threads à la fermeture de l'application"""
        if self.current_thread and self.current_thread.isRunning():
            self.current_thread.stop()
            self.current_thread.wait(1000)  # Attendre 1 seconde pour la fin du thread
        
        for thread in self.threads:
            if thread.isRunning():
                thread.stop()
                thread.wait(1000)
        
        event.accept()


# Main execution block
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Style moderne
    
    window = JiraChachouExporter()
    window.show()
    
    # Capture les exceptions non gérées
    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)
    
    sys._excepthook = sys.excepthook
    sys.excepthook = exception_hook
    
    sys.exit(app.exec_())

