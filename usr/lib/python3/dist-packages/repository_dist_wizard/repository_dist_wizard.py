#!/usr/bin/python3 -u

## Copyright (C) 2014 troubadour <trobador@riseup.net>
## Copyright (C) 2014 - 2023 ENCRYPTED SUPPORT LP <adrelanos@whonix.org>
## See the file COPYING for copying conditions.

import sys
import signal

from PyQt5 import QtCore, QtGui
from subprocess import call

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import *

import os
import inspect
import yaml

from guimessages.translations import _translations
from guimessages.guimessage import gui_message

if os.path.exists('/usr/share/whonix/marker'):
    project = "Whonix"
else:
    project = "Kicksecure"

class common:
    tr_file ='/usr/share/translations/repository-dist.yaml'

class repository_dist_wizard(QWizard):
    def __init__(self):
        super(repository_dist_wizard, self).__init__()

        self.resize(500, 330)
        self.setWindowTitle(project + ' Repository Wizard')
        icon = "/usr/share/icons/icon-pack-dist/whonix.ico"
        self.setWindowIcon(QtGui.QIcon(icon))

        translation = _translations(common.tr_file, 'repository-dist')
        # gettext like.
        self._ = translation.gettext

        # Set a transparent (default dialog) background for the widget.
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 244, 244))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.setPalette(palette)

        self.page_enable = QWizardPage()
        self.enable_group = QGroupBox(self.page_enable)
        self.enable_button = QRadioButton(self.enable_group)
        self.disable_button = QRadioButton(self.enable_group)
        self.addPage(self.page_enable)

        self.page_repos = QWizardPage()
        self.repo_text = QLabel(self.page_repos)
        self.repo_group = QGroupBox(self.page_repos)
        self.repo1 = QRadioButton(self.repo_group)
        self.repo2 = QRadioButton(self.repo_group)
        self.repo3 = QRadioButton(self.repo_group)
        self.repo4 = QRadioButton(self.repo_group)
        self.addPage(self.page_repos)

        self.page_finish = QWizardPage()
        self.finish_text = QLabel(self.page_finish)
        self.addPage(self.page_finish)

        self.one_shot = True

        self.setupUi()

    def setupUi(self):
        self.enable_text = QLabel(self.page_enable)
        self.enable_text.setGeometry(QtCore.QRect(10, 10, 445, 200))
        self.enable_text.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.enable_text.setWordWrap(True)
        self.enable_group.setGeometry(QtCore.QRect(10, 170, 445, 70))
        self.enable_button.setGeometry(QtCore.QRect(30, 22, 400, 21))
        self.enable_button.setChecked(True)
        self.disable_button.setGeometry(QtCore.QRect(30, 42, 300, 21))

        self.repo_text = QLabel(self.page_repos)
        self.repo_text.setGeometry(QtCore.QRect(10, 10, 430, 140))
        self.repo_text.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.repo_text.setWordWrap(True)
        self.repo_group.setGeometry(QtCore.QRect(10, 150, 445, 105))
        self.repo1.setGeometry(QtCore.QRect(30, 20, 300, 21))
        self.repo1.setChecked(True)
        self.repo2.setGeometry(QtCore.QRect(30, 40, 300, 21))
        self.repo3.setGeometry(QtCore.QRect(30, 60, 300, 21))
        self.repo4.setGeometry(QtCore.QRect(30, 80, 300, 21))

        self.finish_text.setGeometry(QtCore.QRect(10, 10, 445, 140))
        self.finish_text.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.finish_text.setWordWrap(True)

        try:
            message = self._('enabletext')
            self.enable_text.setText(message)
            message = self._('repotext')
            self.repo_text.setText(message)
            message = self._('enablebutton_text')
            self.enable_button.setText(message)
            message = self._('disablebutton_text')
            self.disable_button.setText(message)
            message = self._('finish_enabled')
            self.finish_text_disabled = message
            message = self._('finish_disabled')
            self.finish_text_enabled = message
            message = self._('finish_failed')
            self.finish_text_failed = message
        except (yaml.scanner.ScannerError, yaml.parser.ParserError):
            pass

        self.repo_group.setTitle("Repository")
        self.repo1.setText(project + " Stable Repository")
        self.repo2.setText(project + " Stable Proposed Updates Repository")
        self.repo3.setText(project + " Testers Repository")
        self.repo4.setText(project + " Developers Repository")

        self.button(QWizard.BackButton).clicked.connect(self.BackButton_clicked)

        self.exec_()

    """ re-arm command. """
    def BackButton_clicked(self):
        self.button(QWizard.CancelButton).setEnabled(True)
        if not self.one_shot:
            self.one_shot = True

    """ Non-linear wizard. Override QWizard.nextId(). """
    def nextId(self):
        if self.currentId() < 2:
            if self.enable_button.isChecked():
                return self.currentId() + 1

            elif self.disable_button.isChecked():
                if self.one_shot:
                    command = ['pkexec', 'repository-dist', '--disable']
                    exit_code = call(command)
                    mypath = inspect.getfile(inspect.currentframe())

                    if exit_code == 0:
                        self.finish_text.setText(self.finish_text_disabled)
                        message = 'INFO %s: Ok, exit code of "%s" was %s.' % ( mypath, ' '.join(command), exit_code )

                    else:
                        if exit_code == 126:
                            error = '<p>ERROR: Authorization failed.</p>'
                        else:
                            error = '<p>ERROR %s: exit code of \"%s\" was %s.</p>' % ( mypath, ' '.join(command), exit_code )
                        finish_text_failed =  error + self.finish_text_failed
                        self.finish_text.setText(finish_text_failed)
                        message = error

                    print(message)
                    self.one_shot = False

                return self.currentId() + 2

        elif self.currentId() == 2:
            if self.repo1.isChecked():
                repository = ['--repository', 'stable']

            elif self.repo2.isChecked():
                repository = ['--repository', 'stable-proposed-updates']

            elif self.repo3.isChecked():
                repository = ['--repository', 'testers']

            elif self.repo4.isChecked():
                repository = ['--repository', 'developers']

            if self.one_shot:
                command = ['pkexec', 'repository-dist', '--enable'] + repository

                QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
                exit_code = call(command)
                QApplication.restoreOverrideCursor()

                mypath = inspect.getfile(inspect.currentframe())

                if exit_code == 0:
                    self.finish_text.setText(self.finish_text_enabled)
                    message = "INFO %s: Ok, exit code of \"%s\" was %s." % ( mypath, ' '.join(command), exit_code )

                else:
                    if exit_code == 126:
                        error = '<p>ERROR: Authorization failed.</p>'
                    else:
                        error = '<p>ERROR %s: exit code of \"%s\" was %s.</p>' % ( mypath, ' '.join(command), exit_code )
                    finish_text_failed =  error + self.finish_text_failed
                    self.finish_text.setText(finish_text_failed)
                    message = error

                print(message)
                self.one_shot = False

            self.button(QWizard.CancelButton).setEnabled(False)
            return -1
        else:
            return -1

def signal_handler(sig, frame):
    sys.exit(128 + sig)

def main():
    app = QApplication(sys.argv)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    timer = QtCore.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    wizard = repository_dist_wizard()

    sys.exit(0)

if __name__ == "__main__":
    main()
