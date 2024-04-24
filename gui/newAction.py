from PyQt5.QtWidgets import QMessageBox

class NewAction:

    @staticmethod
    def show_confirmation_dialog():
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle('Create new file')
        msg_box.setText('Are you sure you want to create a new file? Unsaved progress may be lost.')
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        
        return_value = msg_box.exec()
        return return_value == QMessageBox.Yes