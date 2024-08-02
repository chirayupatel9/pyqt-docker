import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QMessageBox, QTextEdit, QStackedWidget
)
from datafed.CommandLib import API


class LoginWindow(QWidget):
    def __init__(self, df_api, main_window):
        super().__init__()
        self.df_api = df_api
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle('DataFed Login')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.label_user = QLabel('Username:', self)
        self.username = QLineEdit(self)

        self.label_password = QLabel('Password:', self)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.check_login)

        layout.addWidget(self.label_user)
        layout.addWidget(self.username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.password)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def check_login(self):
        username = self.username.text()
        password = self.password.text()

        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter both username and password')
            return

        try:
            self.df_api.loginByPassword(username, password)
            QMessageBox.information(self, 'Success', 'Login Successful!')
            self.main_window.show()
            self.close()
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Invalid username or password: {e}')


class MainWindow(QWidget):
    def __init__(self, df_api):
        super().__init__()
        self.df_api = df_api
        self.initUI()

    def initUI(self):
        self.setWindowTitle('DataFed Main Window')
        self.setGeometry(100, 100, 800, 600)

        self.stack = QStackedWidget(self)
        self.menu_widget = self.create_menu()
        self.stack.addWidget(self.menu_widget)

        self.create_widget = self.create_record_page()
        self.stack.addWidget(self.create_widget)

        self.read_widget = self.read_record_page()
        self.stack.addWidget(self.read_widget)

        self.update_widget = self.update_record_page()
        self.stack.addWidget(self.update_widget)

        self.delete_widget = self.delete_record_page()
        self.stack.addWidget(self.delete_widget)

        self.transfer_widget = self.transfer_data_page()
        self.stack.addWidget(self.transfer_widget)

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)

    def create_menu(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.label = QLabel('Main Application Window', self)
        layout.addWidget(self.label)

        self.create_button = QPushButton('Create Record', self)
        self.create_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.create_widget))
        layout.addWidget(self.create_button)

        self.read_button = QPushButton('Read Record', self)
        self.read_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.read_widget))
        layout.addWidget(self.read_button)

        self.update_button = QPushButton('Update Record', self)
        self.update_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.update_widget))
        layout.addWidget(self.update_button)

        self.delete_button = QPushButton('Delete Record', self)
        self.delete_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.delete_widget))
        layout.addWidget(self.delete_button)

        self.transfer_button = QPushButton('Transfer Data', self)
        self.transfer_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.transfer_widget))
        layout.addWidget(self.transfer_button)

        self.logout_button = QPushButton('Logout', self)
        self.logout_button.clicked.connect(self.df_logout)
        layout.addWidget(self.logout_button)

        widget.setLayout(layout)
        return widget

    def create_record_page(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.label_create = QLabel('Create Record')
        layout.addWidget(self.label_create)

        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText('Title')
        layout.addWidget(self.title_input)

        self.metadata_input = QTextEdit(self)
        self.metadata_input.setPlaceholderText('Metadata (JSON format)')
        layout.addWidget(self.metadata_input)

        self.context_input = QLineEdit(self)
        self.context_input.setPlaceholderText('Context (optional)')
        layout.addWidget(self.context_input)

        self.create_record_button = QPushButton('Create Record', self)
        self.create_record_button.clicked.connect(self.create_record)
        layout.addWidget(self.create_record_button)

        self.back_button = QPushButton('Back', self)
        self.back_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.menu_widget))
        layout.addWidget(self.back_button)

        widget.setLayout(layout)
        return widget

    def read_record_page(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.label_read = QLabel('Read Record')
        layout.addWidget(self.label_read)

        self.record_id_input = QLineEdit(self)
        self.record_id_input.setPlaceholderText('Record ID')
        layout.addWidget(self.record_id_input)

        self.read_button = QPushButton('Read Record', self)
        self.read_button.clicked.connect(self.read_record)
        layout.addWidget(self.read_button)

        self.read_output = QTextEdit(self)
        self.read_output.setReadOnly(True)
        layout.addWidget(self.read_output)

        self.back_button = QPushButton('Back', self)
        self.back_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.menu_widget))
        layout.addWidget(self.back_button)

        widget.setLayout(layout)
        return widget

    def update_record_page(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.label_update = QLabel('Update Record')
        layout.addWidget(self.label_update)

        self.update_id_input = QLineEdit(self)
        self.update_id_input.setPlaceholderText('Record ID')
        layout.addWidget(self.update_id_input)

        self.update_metadata_input = QTextEdit(self)
        self.update_metadata_input.setPlaceholderText('Metadata (JSON format)')
        layout.addWidget(self.update_metadata_input)

        self.update_button = QPushButton('Update Record', self)
        self.update_button.clicked.connect(self.update_record)
        layout.addWidget(self.update_button)

        self.back_button = QPushButton('Back', self)
        self.back_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.menu_widget))
        layout.addWidget(self.back_button)

        widget.setLayout(layout)
        return widget

    def delete_record_page(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.label_delete = QLabel('Delete Record')
        layout.addWidget(self.label_delete)

        self.delete_id_input = QLineEdit(self)
        self.delete_id_input.setPlaceholderText('Record ID')
        layout.addWidget(self.delete_id_input)

        self.delete_button = QPushButton('Delete Record', self)
        self.delete_button.clicked.connect(self.delete_record)
        layout.addWidget(self.delete_button)

        self.back_button = QPushButton('Back', self)
        self.back_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.menu_widget))
        layout.addWidget(self.back_button)

        widget.setLayout(layout)
        return widget

    def transfer_data_page(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.label_transfer = QLabel('Transfer Data')
        layout.addWidget(self.label_transfer)

        self.source_id_input = QLineEdit(self)
        self.source_id_input.setPlaceholderText('Source ID')
        layout.addWidget(self.source_id_input)

        self.dest_collection_input = QLineEdit(self)
        self.dest_collection_input.setPlaceholderText('Destination Collection')
        layout.addWidget(self.dest_collection_input)

        self.transfer_button = QPushButton('Transfer Data', self)
        self.transfer_button.clicked.connect(self.transfer_data)
        layout.addWidget(self.transfer_button)

        self.back_button = QPushButton('Back', self)
        self.back_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.menu_widget))
        layout.addWidget(self.back_button)

        widget.setLayout(layout)
        return widget

    def create_record(self):
        title = self.title_input.text()
        metadata = self.metadata_input.toPlainText()
        context = self.context_input.text()

        if not title or not metadata:
            QMessageBox.warning(self, 'Error', 'Title and metadata are required')
            return

        try:
            if context:
                self.df_api.setContext(context)
            response = self.df_api.dataCreate(title, metadata=metadata)
            res = self.to_dict(str(response[0].data[0]))
            QMessageBox.information(self, 'Success', f'Record created: {res}')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to create record: {e}')

    def read_record(self):
        record_id = self.record_id_input.text()

        if not record_id:
            QMessageBox.warning(self, 'Error', 'Record ID is required')
            return

        try:
            response = self.df_api.dataView(f"d/{record_id}")
            res = self.to_dict(str(response[0].data[0]))
            self.read_output.setText(str(res))
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to read record: {e}')

    def update_record(self):
        record_id = self.update_id_input.text()
        metadata = self.update_metadata_input.toPlainText()

        if not record_id or not metadata:
            QMessageBox.warning(self, 'Error', 'Record ID and metadata are required')
            return

        try:
            response = self.df_api.dataUpdate(f"d/{record_id}", metadata=metadata)
            res = self.to_dict(str(response[0].data[0]))
            QMessageBox.information(self, 'Success', f'Record updated: {res}')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to update record: {e}')

    def delete_record(self):
        record_id = self.delete_id_input.text()

        if not record_id:
            QMessageBox.warning(self, 'Error', 'Record ID is required')
            return

        try:
            self.df_api.dataDelete(f"d/{record_id}")
            QMessageBox.information(self, 'Success', 'Record successfully deleted')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to delete record: {e}')

    def transfer_data(self):
        source_id = self.source_id_input.text()
        dest_collection = self.dest_collection_input.text()

        if not source_id or not dest_collection:
            QMessageBox.warning(self, 'Error', 'Source ID and destination collection are required')
            return

        try:
            # Retrieve source data record details
            source_record = self.df_api.dataView(f"d/{source_id}")
            source_details = source_record[0].data[0]

            # Create a new record in the destination collection
            new_record = self.df_api.dataCreate(
                title=source_details.title,
                metadata=source_details.metadata,
                parent=dest_collection
            )
            new_record_id = new_record[0].data[0].id

            # Transfer the actual data file
            self.df_api.dataMove(f"d/{source_id}", new_record_id)

            QMessageBox.information(self, 'Success', f'Data transferred to new record ID: {new_record_id}')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to transfer data: {e}')

    def df_logout(self):
        try:
            self.df_api.logout()
            self.close()
            self.login_window = LoginWindow(self.df_api, self)
            self.login_window.show()
            QMessageBox.information(self, 'Success', 'Logged out successfully!')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to logout: {e}')

    def to_dict(self, data_str):
        data_dict = {}
        for line in data_str.strip().split('\n'):
            key, value = line.split(": ", 1)
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]  # Remove surrounding quotes
            elif value == 'true':
                value = True
            elif value == 'false':
                value = False
            elif value.isdigit():
                value = int(value)
            data_dict[key] = value
        return data_dict


def main():
    app = QApplication(sys.argv)
    df_api = API()
    main_window = MainWindow(df_api)
    aut = df_api.getAuthUser()
    print(aut)
    if df_api.getAuthUser():
        main_window.show()
    else:
        login = LoginWindow(df_api, main_window)
        login.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
