import psycopg2
import config
import sys

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QTabWidget,
    QAbstractScrollArea,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QGroupBox,
    QTableWidgetItem,
    QPushButton,
    QMessageBox,
    QComboBox,
    QInputDialog,
    QDialog,
)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.selected_day = 0
        self.selected_even = True
        self._connect_to_db()
        self.setWindowTitle("Расписание")
        self.vbox = QVBoxLayout(self)
        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)
        self._create_shedule_tab()
        self._create_teacher_tab()
        self._create_subject_tab()

    def setColortoRow(self, table, rowIndex, color):
        try:
            for j in range(table.columnCount()):
                table.item(rowIndex, j).setBackground(color)
        except:
            pass

    def handle_day_Activated(self, index):
        self.selected_day = self.day_selector.itemData(index)
        self._update_shedule_table()

    def handle_even_Activated(self, index):
        self.selected_even = self.even_selector.itemData(index)
        self._update_shedule_table()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(
            database=config.db_connect["database"],
            user=config.db_connect["user"],
            password=config.db_connect["password"],
            host=config.db_connect["host"],
            port=config.db_connect["port"],
        )
        self.cursor = self.conn.cursor()

    def _create_shedule_tab(self):
        self.shedule_tab = QWidget()
        self.tabs.addTab(self.shedule_tab, "Расписание")
        self.day_gbox = QGroupBox("Расписание")
        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()
        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)
        self.shbox1.addWidget(self.day_gbox)
        self._create_shedule_table()
        self.update_shedule_button = QPushButton("Записать всю базу")
        self.refresh = QPushButton("Обновить таблицу")
        self.shbox2.addWidget(self.refresh)
        self.refresh.clicked.connect(self._update_shedule_table)
        self.day_selector = QComboBox(self)

        for indx, text in enumerate(config.buttons["day_menu"]):
            self.day_selector.addItem(text, indx)
        self.even_selector = QComboBox(self)

        for indx, text in enumerate(config.buttons["odd_menu"]):
            self.even_selector.addItem(text, indx)
        self.day_selector.activated.connect(self.handle_day_Activated)
        self.even_selector.activated.connect(self.handle_even_Activated)
        self.shbox2.addWidget(self.day_selector)
        self.shbox2.addWidget(self.even_selector)
        self.shbox2.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._rewrite_all_shedule)
        self.shedule_tab.setLayout(self.svbox)

    def _create_teacher_tab(self):
        self.teacher_tab = QWidget()
        self.tabs.addTab(self.teacher_tab, "Преподаватели")
        self.day_gbox = QGroupBox("Преподаватели")
        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()
        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)
        self.shbox1.addWidget(self.day_gbox)
        self._create_teacher_table()
        self.update_teacher_button = QPushButton("Записать всю базу")
        self.refresh = QPushButton("Обновить таблицу")
        self.shbox2.addWidget(self.refresh)
        self.refresh.clicked.connect(self._update_teacher_table)
        self.shbox2.addWidget(self.update_teacher_button)
        self.update_teacher_button.clicked.connect(self._rewrite_all_teacher)
        self.teacher_tab.setLayout(self.svbox)

    def _create_teacher_table(self):
        self.teacher_table = QTableWidget()
        self.teacher_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.teacher_table.setColumnCount(5)
        self.teacher_table.setColumnHidden(4, True)
        self.teacher_table.setHorizontalHeaderLabels(
            ["ФИО", "Предмет", "", ""]
        )
        self._update_teacher_table()
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.teacher_table)
        self.day_gbox.setLayout(self.mvbox)

    def _update_teacher_table(self):
        self.cursor.execute("SELECT * FROM bin2001.teacher")
        records = list(self.cursor.fetchall())
        self.teacher_table.setRowCount(0)
        self.teacher_table.setRowCount(len(records) + 1)
        self.cursor.execute("SELECT subject FROM bin2001.subject")
        records1 = list(self.cursor.fetchall())
        subjects_list = []
        for i in records1:
            subjects_list.append((str(i[0])[1:-1]).replace('"',""))
        for i, r in enumerate(records):
            r = list(r)
            subject_records = list(map(lambda x: str(x[2]), records))
            teacher_records = list(map(lambda x: str(x[1]), records))
            subjects = list()
            teachers = list()
            try:
                subject_selector = QComboBox()
                subjects.append(str(r[2]))
                subjects.extend(subjects_list)
            except:
                pass
            try:
                teacher_selector = QComboBox()
                teacher_records.remove(str(r[1]))
                teachers.append(str(r[1]))
                teachers.extend(subject_records)
            except:
                pass
            subject_selector.addItems(subjects)
            teacher_selector.addItems(teachers)
            joinButton = QPushButton("Обновить")
            deleteButton = QPushButton("Удалить")
            self.teacher_table.setItem(i, 0, QTableWidgetItem(r[1]))
            self.teacher_table.setCellWidget(i, 1, subject_selector)
            self.teacher_table.setCellWidget(i, 2, joinButton)
            self.teacher_table.setCellWidget(i, 3, deleteButton)
            self.teacher_table.setItem(i, 4, QTableWidgetItem(str(r[0])))
            db_row_id = r[0]
            joinButton.clicked.connect(
                lambda ch, i=i, r=r, db_row_id=db_row_id: self._change_teacher_from_table(
                    i, r, db_row_id
                )
            )
            deleteButton.clicked.connect(
                lambda ch, i=i, r=r, db_row_id=db_row_id: self._delete_teacher_from_table(
                    i, r, db_row_id
                )
            )
        subject_selectors = QComboBox()
        subject_selectors.addItems(subjects_list)
        self.teacher_table.setCellWidget(i+1, 1, subject_selectors)
        insertButton = QPushButton("Внести")
        self.teacher_table.setCellWidget(i + 1, 2, insertButton)
        insertButton.clicked.connect(
            lambda ch, i=i + 1: self._insert_teacher_from_table(
                i
            )
        )
        self.teacher_table.resizeRowsToContents()

    def _create_shedule_table(self):
        self.shedule_table = QTableWidget()
        self.shedule_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.shedule_table.setColumnCount(6)
        self.shedule_table.setColumnHidden(5, True)
        self.shedule_table.setHorizontalHeaderLabels(
            ["Предмет", "Начало пары", "Кабинет", "", ""]
        )
        self._update_shedule_table()
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.shedule_table)
        self.day_gbox.setLayout(self.mvbox)

    def _update_shedule_table(self):
        self.cursor.execute(
            "SELECT * FROM bin2001.timetable WHERE day = %s AND is_even = %s ORDER BY start_time",
            (int(self.selected_day), bool(self.selected_even)),
        )
        records = list(self.cursor.fetchall())
        self.shedule_table.setRowCount(0)
        if len(records) < 5:
            self.shedule_table.setRowCount(len(records) + 1)
        else:
            self.shedule_table.setRowCount(len(records))
        self.cursor.execute(
            "SELECT DISTINCT start_time FROM bin2001.timetable ORDER BY start_time"
        )
        time_record = list(self.cursor.fetchall())
        self.cursor.execute("SELECT DISTINCT name FROM bin2001.subject")
        subject_record = list(self.cursor.fetchall())
        for i, r in enumerate(records):
            r = list(r)
            time_records = list(map(lambda x: str(x[0])[:-3], time_record))
            subject_records = list(map(lambda x: str(x[0]), subject_record))
            subjects = list()
            times = list()
            joinButton = QPushButton("Обновить")
            deleteButton = QPushButton("Удалить")
            try:
                subject_selector = QComboBox()
                subject_records.remove(str(r[2]))
                subjects.append(str(r[2]))
                subjects.extend(subject_records)
            except:
                pass
            try:
                times_selector = QComboBox()
                time_records.remove(str(r[4])[:-3])
                times.append(str(r[4])[:-3])
                times.extend(time_records)
            except:
                pass
            subject_selector.addItems(subjects)
            times_selector.addItems(times)
            self.shedule_table.setCellWidget(i, 0, subject_selector)
            self.shedule_table.setCellWidget(i, 1, times_selector)
            self.shedule_table.setItem(i, 2, QTableWidgetItem(r[3]))
            self.shedule_table.setCellWidget(i, 3, joinButton)
            self.shedule_table.setCellWidget(i, 4, deleteButton)
            self.shedule_table.setItem(i, 5, QTableWidgetItem(str(r[0])))
            db_row_id = r[0]
            joinButton.clicked.connect(
                lambda ch, i=i, r=r, db_row_id=db_row_id: self._change_shedule_from_table(
                    i, r, db_row_id
                )
            )
            deleteButton.clicked.connect(
                lambda ch, db_row_id=db_row_id: self._delete_shedule_from_table(
                    db_row_id
                )
            )

        if len(records) < 5:
            subject_selector = QComboBox()
            times_selector = QComboBox()
            subject_selector.addItems(subjects)
            times_selector.addItems(times)
            insertButton = QPushButton("Внести")
            self.shedule_table.setCellWidget(i + 1, 0, subject_selector)
            self.shedule_table.setCellWidget(i + 1, 1, times_selector)
            self.shedule_table.setCellWidget(i + 1, 3, insertButton)
            insertButton.clicked.connect(
                lambda ch, i=i + 1: self._insert_shedule_from_table(
                    i
                )
            )

        self.shedule_table.resizeRowsToContents()

    def _create_subject_tab(self):
        self.subject_tab = QWidget()
        self.tabs.addTab(self.subject_tab, "Предметы")
        self.day_gbox = QGroupBox("Предметы")
        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()
        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)
        self.shbox1.addWidget(self.day_gbox)
        self._create_subject_table()
        self.update_subject_button = QPushButton("Записать всю базу")
        self.refresh = QPushButton("Обновить таблицу")
        self.shbox2.addWidget(self.refresh)
        self.refresh.clicked.connect(self._update_subject)
        self.shbox2.addWidget(self.update_subject_button)
        self.subject_tab.setLayout(self.svbox)

    def _create_subject_table(self):
        self.subject_table = QTableWidget()
        self.subject_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.subject_table.setColumnCount(5)
        self.subject_table.setColumnHidden(4, True)
        self.subject_table.setHorizontalHeaderLabels(
            ["Премет", "", "", ""]
        )
        self._update_subject_table()
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.subject_table)
        self.day_gbox.setLayout(self.mvbox)

    def _update_subject_table(self):
        self.cursor.execute("SELECT * FROM bin2001.subject")
        records = list(self.cursor.fetchall())
        self.subject_table.setRowCount(0)
        self.subject_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            subject_records = list(map(lambda x: str(x[0]), records))
            subjects = list()
            joinButton = QPushButton("Обновить")
            deleteButton = QPushButton("Удалить")
            try:
                subject_selector = QComboBox()
                subject_records.remove(str(r[0]))
                subjects.append(str(r[0]))
                subjects.extend(subject_records)

            except:
                pass

            subject_selector.addItems(subjects)
            self.shedule_table.setCellWidget(i, 0, subject_selector)
            # joinButton = QPushButton("Обновить")
            # deleteButton = QPushButton("Удалить")
            self.subject_table.setItem(i, 0, QTableWidgetItem(r[0]))
            # self.subject_table.setCellWidget(i, 1, subject_selector)
            self.subject_table.setCellWidget(i, 1, joinButton)
            self.subject_table.setCellWidget(i, 2, deleteButton)
            # self.subject_table.setItem(i, 3, QTableWidgetItem(str(r[0])))
            db_row_id = r[0]

            joinButton.clicked.connect(
                lambda ch, i=i, r=r, db_row_id=db_row_id: self._change_subject_from_table(
                    i, r, db_row_id
                )
            )
            deleteButton.clicked.connect(
                lambda ch, i=i, r=r, db_row_id=db_row_id: self._delete_subject_from_table(
                    i, r, db_row_id
                )
            )
        insertButton = QPushButton("Внести")
        self.subject_table.setCellWidget(i + 1, 1, insertButton)
        insertButton.clicked.connect(
            lambda ch, i=i + 1: self._insert_subject_from_table(
                i
            )
        )
        self.subject_table.resizeRowsToContents()

    def _change_subject_from_table(self, rowNum, row, db_row_id):
        row = list()
        for i in range(self.subject_table.columnCount()):
            try:
                row.append(self.subject_table.item(rowNum, i).text())
            except AttributeError:
                try:
                    row.append(self.subject_table.cellWidget(rowNum, i).currentText())
                except:
                    row.append(None)
        try:
            self.cursor.execute(
                "UPDATE bin2001.subject SET name = %s",
                (row[0], db_row_id),
            )
            self.conn.commit()
        except Exception as e:
            QMessageBox.about(self, "Error", str(e))

    def _change_teacher_from_table(self, rowNum, row, db_row_id):
        row = list()
        for i in range(self.teacher_table.columnCount()):
            try:
                row.append(self.teacher_table.item(rowNum, i).text())
            except AttributeError:
                try:
                    row.append(self.teacher_table.cellWidget(rowNum, i).currentText())
                except:
                    row.append(None)
        try:
            self.cursor.execute(
                "UPDATE bin2001.teacher SET full_name = %s WHERE id = %s",
                (row[0], db_row_id),
            )
            self.conn.commit()

        except Exception as e:
            QMessageBox.about(self, "Error", str(e))

    def _change_shedule_from_table(self, rowNum, row, db_row_id):
        row = list()
        for i in range(self.shedule_table.columnCount()):
            try:
                row.append(self.shedule_table.item(rowNum, i).text())
            except AttributeError:
                try:
                    row.append(self.shedule_table.cellWidget(rowNum, i).currentText())
                except:
                    row.append(None)
        try:
            self.cursor.execute(
                "UPDATE bin2001.timetable SET subject = %s, start_time = %s WHERE id = %s",
                (row[0], row[1], db_row_id),
            )
            self.conn.commit()
        except Exception as e:
            QMessageBox.about(self, "Error", str(e))

    def _add_new_subject(self, subject):
        try:
            self.cursor.execute(
                "INSERT INTO bin2001.subject (name) VALUES (%s)", (str(subject),)
            )

            self.conn.commit()
            self._update_subject()
            self._update_shedule()
        except Exception as e:
            QMessageBox.about(self, "Error", str(e))

    def _add_new_teacher(self, full_name, subject):
        try:
            self.cursor.execute(
                "INSERT INTO bin2001.teacher (full_name, subject) VALUES (%s, %s)",(str(full_name), str(subject)),)
            self.conn.commit()
            self._update_teacher()
            self._update_shedule()
        except Exception as e:
            QMessageBox.about(self, "Error", str(e))

    def _add_new_day_subject(self, subject, room_numb, start_time):
        try:
            self.cursor.execute(
                "INSERT INTO bin2001.timetable (day, subject, room_numb, start_time, is_even) VALUES (%s, %s, %s, %s, %s)",
                (
                    str(self.selected_day),
                    str(subject),
                    str(room_numb),
                    str(start_time),
                    self.selected_even,
                ),
            )
            self.conn.commit()
            self._update_teacher()
            self._update_shedule()
        except Exception as e:
            QMessageBox.about(self, "Error", str(e))

    def _delete_subject_from_table(self, rowNum, row, db_row_id):
        row = list()
        for i in range(self.subject_table.columnCount()):
            try:
                row.append(self.subject_table.item(rowNum, i).text())
            except AttributeError:
                try:
                    row.append(self.subject_table.cellWidget(rowNum, i).currentText())
                except:
                    row.append(None)
        try:
            self.cursor.execute(
                "DELETE FROM bin2001.subject WHERE name = %s", (row[0],)
            )

            self.conn.commit()
            self._update_subject()
        except Exception as e:
            QMessageBox.about(self, "Error", str(e))

    def _delete_teacher_from_table(self, rowNum, row, db_row_id):
        row = list()
        for i in range(self.teacher_table.columnCount()):
            try:
                row.append(self.teacher_table.item(rowNum, i).text())
            except AttributeError:
                try:
                    row.append(self.teacher_table.cellWidget(rowNum, i).currentText())
                except:
                    row.append(None)
        try:
            self.cursor.execute(
                "DELETE FROM bin2001.teacher WHERE full_name = %s", (row[0],)
            )
            self.cursor.execute(
                "DELETE FROM bin2001.subject WHERE name = %s", (row[1],)
            )
            self.conn.commit()
            self._update_teacher()
        except Exception as e:
            QMessageBox.about(self, "Error", str(e))

    def _delete_shedule_from_table(self, db_row_id):
        try:
            self.cursor.execute(
                "DELETE FROM bin2001.timetable WHERE id = %s", (db_row_id,)
            )
            self.conn.commit()
            self._update_shedule()
        except Exception as e:
            QMessageBox.about(self, "Error", str(e))

    def _rewrite_all_subject(self):
        try:
            for i in range(self.subject_table.rowCount()):
                row = []
                for j in range(self.subject_table.columnCount()):
                    try:
                        row.append(self.subject_table.item(i, j).text())
                    except AttributeError:
                        try:
                            row.append(
                                self.subject_table.cellWidget(i, j).currentText()
                            )
                        except:
                            row.append(None)
                self.cursor.execute(
                    """
                    UPDATE bin2001.subject
                    SET name = %s

                    """,
                    (row[0]),
                )
            self.conn.commit()
        except Exception as e:
            QMessageBox.about(self, "Error", str(e))
        else:
            QMessageBox.about(self, "OK", "База успешно перезаписана")

    def _rewrite_all_teacher(self):
        try:
            for i in range(self.teacher_table.rowCount()):
                row = []
                for j in range(self.teacher_table.columnCount()):
                    try:
                        row.append(self.teacher_table.item(i, j).text())
                    except AttributeError:
                        try:
                            row.append(
                                self.teacher_table.cellWidget(i, j).currentText()
                            )
                        except:
                            row.append(None)
                self.cursor.execute(
                    """
                    UPDATE bin2001.teacher
                    SET full_name = %s, subject = %s
                    WHERE id = %s
                    """,
                    (row[0], row[1], row[4]),
                )
            self.conn.commit()
        except Exception as e:
            QMessageBox.about(self, "Error", str(e))
        else:
            QMessageBox.about(self, "OK", "База успешно перезаписана")

    def _rewrite_all_shedule(self):
        try:
            for i in range(self.shedule_table.rowCount()):
                row = []
                for j in range(self.shedule_table.columnCount()):
                    try:
                        row.append(self.shedule_table.item(i, j).text())
                    except AttributeError:
                        try:
                            row.append(
                                self.shedule_table.cellWidget(i, j).currentText()
                            )
                        except:
                            row.append(None)
                # table.append(row)
                self.cursor.execute(
                    """
                    UPDATE bin2001.timetable
                    SET subject = %s, room_numb = %s, start_time = %s
                    WHERE id = %s
                    """,
                    (row[0], row[2], row[1], row[5]),
                )
            self.conn.commit()
        except Exception as e:
            QMessageBox.about(self, "Error", str(e))
        else:
            QMessageBox.about(self, "OK", "База успешно перезаписана")

    def _insert_shedule_from_table(self, rowNum):
        row = list()
        for i in range(self.shedule_table.columnCount()):
            try:
                row.append(self.shedule_table.item(rowNum, i).text())
            except AttributeError:
                try:
                    row.append(self.shedule_table.cellWidget(rowNum, i).currentText())
                except:
                    row.append(None)
        if row[0] == None or row[1] == None or row[2] == None:
            QMessageBox.about(self, "Error", "Необходимо ввести данные")
        else:
            self.shedule_table.setItem(rowNum, 0, QTableWidgetItem(''))
            self.shedule_table.setItem(rowNum, 1, QTableWidgetItem(''))
            self.shedule_table.setItem(rowNum, 2, QTableWidgetItem(''))
            self._add_new_day_subject(row[0], row[2], row[1])

    def _insert_subject_from_table(self, rowNum):
        row = list()
        for i in range(self.subject_table.columnCount()):
            try:
                row.append(self.subject_table.item(rowNum, i).text())
            except AttributeError:
                try:
                    row.append(self.subject_table.cellWidget(rowNum, i).currentText())
                except:
                    row.append(None)
        if row[0] == None:
            QMessageBox.about(self, "Error", "Необходимо ввести данные")
        else:
            self.subject_table.setItem(rowNum, 0, QTableWidgetItem(''))
            self._add_new_subject(row[0])

    def _insert_teacher_from_table(self, rowNum):
        row = list()
        for i in range(self.teacher_table.columnCount()):
            try:
                row.append(self.teacher_table.item(rowNum, i).text())
            except AttributeError:
                try:
                    row.append(self.teacher_table.cellWidget(rowNum, i).currentText())
                except:
                    row.append(None)
        if row[0] == None or row[1] == None:
            QMessageBox.about(self, "Error", "Необходимо ввести данные")
        else:
            self.teacher_table.setItem(rowNum, 0, QTableWidgetItem(''))
            self.teacher_table.setItem(rowNum, 1, QTableWidgetItem(''))
            self._add_new_teacher(row[0], row[1])

    def _update_shedule(self):
        self._update_shedule_table()

    def _update_teacher(self):
        self._update_teacher_table()

    def _update_subject(self):
        self._update_subject_table()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())