# coding=utf-8
import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel, QTextEdit,
                             QLineEdit, QApplication, QDesktopWidget, QPushButton, QMainWindow)
from PyQt5.QtGui import QIcon
import ctypes
import img_rc
import vin_to_pc_simu, vin_tool, pc_simu_to_vin


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        ver = 1.3
        self.in_vin_lbl = QLabel('vin:', self)
        self.in_hex_lbl = QLabel('hex:', self)

        self.in_vin_edit = QLineEdit(self)  # 输入框
        self.in_vin_edit.setMaxLength(17)
        self.in_hex_edit = QLineEdit(self)
        self.in_hex_edit.setMaxLength(51)

        self.button = QPushButton('Start', self)
        self.button_clear = QPushButton('Clear', self)

        self.out_ = QTextEdit()
        self.out_lbl = QLabel('odb_cmd:', self)
        self.statusBar = self.statusBar()
        self.statusBar.showMessage('Waiting for input...  (注：在vin栏输入"HELP"点击"Start"，可获取帮助信息')

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.in_vin_lbl, 0, 0)
        grid.addWidget(self.in_vin_edit, 0, 1)

        grid.addWidget(self.in_hex_lbl, 1, 0)
        grid.addWidget(self.in_hex_edit, 1, 1)

        grid.addWidget(self.button, 1, 3)
        grid.addWidget(self.button_clear, 0, 3)

        grid.addWidget(self.out_lbl, 2, 0, 1, 1)
        grid.addWidget(self.out_, 2, 1, 1, 1)

        main_frame = QWidget()
        main_frame.setLayout(grid)
        self.setCentralWidget(main_frame)

        self.resize(500, 350)  # 宽，长
        self.center()
        self.setWindowTitle('vin码转换工具_v' + str(ver))  # 窗口标题
        # self.setWindowIcon(QIcon('icon.png'))  # 图标
        self.setWindowIcon(QIcon(':/icon.png'))  # 图标
        # ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('icon.png')
        # ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(':/icon.png')
        self.show()

        self.button.clicked.connect(self.onChanged)
        self.button_clear.clicked.connect(self.clear_input)

    def center(self):

        qr = self.frameGeometry()  # 获得主窗口的一个矩形特定几何图形。这包含了窗口的框架。
        cp = QDesktopWidget().availableGeometry().center()  # 显示器的绝对值的中心点
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def clear_input(self):
        self.in_vin_edit.setText('')
        self.in_hex_edit.setText('')
        self.out_.setText('')
        self.statusBar.showMessage('Waiting for input...  (注：在vin栏输入"HELP"点击"Start"，可获取帮助信息')

    def onChanged(self):
        if not (self.in_hex_edit.text() or self.in_vin_edit.text() or self.out_.toPlainText()):
            self.statusBar.showMessage('输入为空')

        elif self.in_vin_edit.text():
            if self.in_vin_edit.text().upper() == 'HELP':
                self.in_hex_edit.setText('')
                self.statusBar.showMessage('帮助信息...')
                self.out_.setText('工具说明：\n'
                                  '此工具用于方便转换生成VIN、VIN的十六进制格式、该VIN的OBD回复命令。  ——hml  2019.05.17\n\n'
                                  '使用方法：\n一、已知VIN码，目的为获取VIN的十六进制格式 或 该VIN的OBD回复命令:\n'
                                  '    1、在“vin”栏输入VIN码\n'
                                  '       格式为：\n'
                                  '             LNBMDBAF7GU197436\n'
                                  '    2、点击“Start”\n    '
                                  '\n二、已知VIN码的十六进制格式，目的为获取VIN码 或 该VIN的OBD回复命令:\n'
                                  '    1、在“hex”栏输入VIN码的十六进制格式\n'
                                  '       格式为：\n'
                                  '             4C 4E 42 4D 44 42 41 46 37 47 55 31 39 37 34 33 36\n'
                                  '             （注意每个字节之间有一个空格）\n'
                                  '    2、点击“Start”\n\n'
                                  '三、已知该VIN的OBD回复命令，目的为获取VIN码 或 VIN的十六进制格式:\n'
                                  '    1、在“obd_cmd”栏输入该VIN的OBD回复命令\n'
                                  '       格式为：\n'
                                  '             10 14 5A 90 00 4C 4E 42 \n'
                                  '             21 4D 44 42 41 46 37 47 \n'
                                  '             22 55 31 39 37 34 33 36\n'
                                  '             （标准OBD CAN型回复命令，其中BYTE04到BYTE20为VIN码的十六进制）\n'
                                  '             或是\n'
                                  '             87 F1 11 49 02 01 00 00 00 4C D1 \n'
                                  '             87 F1 11 49 02 02 4E 42 4D 44 D2 \n'
                                  '             87 F1 11 49 02 03 42 41 46 37 D3 \n'
                                  '             87 F1 11 49 02 04 47 55 31 39 D4 \n'
                                  '             87 F1 11 49 02 05 37 34 33 36 D5\n'
                                  '             （标准OBD 串型回复命令，其中第1帧的BYTE09及之后4帧命令的BYTE06-09为VIN码的十六进制） \n'
                                  '    2、点击“Start”\n\n'
                                  '四、清空所有数据：\n    1、点击“Clear”\n\n\n'
                                  '感谢您的使用，如有任何问题，请联系我。  hml 20190719')
                return
            vin, msg = vin_tool.check_vin(self.in_vin_edit.text().upper())
            print(vin)
            if vin:
                self.statusBar.showMessage(msg)

                vin_hex = vin_tool.vin2hex(vin)
                self.in_hex_edit.setText(vin_hex)
                obd_vin_hexs_can = vin_to_pc_simu._can(vin_hex.split(' '))
                obd_vin_hexs_kw = vin_to_pc_simu._kw(vin_hex.split(' '))

                self.out_.setText(' '.join(obd_vin_hexs_can + ['\n'] + obd_vin_hexs_kw).replace('\n ', '\n'))
            else:
                # vin码有错的情况
                self.statusBar.showMessage(msg)
                self.in_hex_edit.setText('')
                self.out_.setText('')
                return

        elif self.in_hex_edit.text():
            # vin无数据，vin_hex有数据

            vin_hex = self.in_hex_edit.text()
            print(vin_hex)
            # vin_old = vin_tool.hex2vin(vin_hex)
            vin_old, status = vin_tool.hex2vin(vin_hex)
            if not status:
                self.statusBar.showMessage(vin_old)
                return

            vin, msg = vin_tool.hex2vin_check_vin(vin_hex)
            if vin:
                self.statusBar.showMessage(msg)

                self.in_vin_edit.setText(vin)

                if ''.join(vin_old) != vin:
                    vin_hex = vin_tool.vin2hex(vin)

                obd_vin_hexs_can = vin_to_pc_simu._can(vin_hex.split(' '))
                obd_vin_hexs_kw = vin_to_pc_simu._kw(vin_hex.split(' '))

                self.out_.setText(' '.join(obd_vin_hexs_can + ['\n'] + obd_vin_hexs_kw).replace('\n ', '\n'))
            else:
                self.statusBar.showMessage(msg)
                return
        elif self.out_.toPlainText():
            # 输入框内有数据
            cmd = self.out_.toPlainText()
            vin_hexs, msg = pc_simu_to_vin.cmd_to_vin_hexs(cmd)
            self.statusBar.showMessage(msg)
            print(vin_hexs)
            vin_hex = ' '.join(vin_hexs)
            vin_old, status = vin_tool.hex2vin(vin_hex)
            if not status:
                self.statusBar.showMessage(vin_old)
                return

            vin, msg = vin_tool.hex2vin_check_vin(vin_hex)
            if vin:
                self.statusBar.showMessage(msg)
                self.in_vin_edit.setText(vin)

                if ''.join(vin_old) != vin:
                    vin_hex = vin_tool.vin2hex(vin)

                self.in_hex_edit.setText(vin_hex)

            else:
                self.statusBar.showMessage(msg)
                return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
