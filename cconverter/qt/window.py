# -*- coding: utf-8 -*-
"""
:Date: Sun Jul 24 18:15:08 CEST 2011
:Authors: Einar Uvsløkk <einar.uvslokk@linux.com>
:Copyright: (c) 2011 Einar Uvsløkk
:License: GNU General Public License (GPL) version 3 or later

vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
"""
import logging
import operator
import sys

from PySide import QtGui

from ..core import (currency, config, app_info as appInfo)
from .Ui_MainWindow import Ui_MainWindow
import resources


class CConverterQtWindow(QtGui.QMainWindow, Ui_MainWindow):
    """Curency Converter Qt4 main window."""
    _log = logging.getLogger(__name__)

    def __init__(self, data, parent=None):
        super(CConverterQtWindow, self).__init__(parent)
        self.setupUi(self)
        self.converter = currency.CurrencyConverter()
        self._initToolBar()
        self._initCalculator()
        self._initComboBoxes()
        self._loadConfig()

    def _initToolBar(self):
        """Due to the lack of required QtDesigner kung-fu knowledge, the
        toolbar must be setup manually.
        """
        self.actionConvert.setIcon(QtGui.QIcon(':/icons/32/convert'))
        self.actionQuit.setIcon(QtGui.QIcon(':/icons/32/exit'))
        self.actionCalc.setIcon(QtGui.QIcon(':/icons/32/calc'))
        self.actionClear.setIcon(QtGui.QIcon(':/icons/32/clear'))
        self.actionHelp.setIcon(QtGui.QIcon(':/icons/32/help_contents'))
        self.actionAbout.setIcon(QtGui.QIcon(':/icons/32/help_about'))

    def _initCalculator(self):
        names = ['7', '8', '9', '/',
                 '4', '5', '6', '*',
                 '1', '2', '3', '-',
                 '0', '.', '=', '+']
        pos = [(0, 0), (0, 1), (0, 2), (0, 3),
               (1, 0), (1, 1), (1, 2), (1, 3),
               (2, 0), (2, 1), (2, 2), (2, 3),
               (3, 0), (3, 1), (3, 2), (3, 3)]

        grid = QtGui.QGridLayout()

        j = 0
        for i in names:
            button = QtGui.QPushButton(i)
            button.clicked.connect(self.onCalcButtonClicked)
            grid.addWidget(button, pos[j][0], pos[j][1])
            j += 1

        self.calculator.setLayout(grid)

    def _initComboBoxes(self):
        cboxes = [self.sourceCombo, self.targetCombo]
        for cbox in cboxes:
            for k, v in sorted(currency.Currencies.items(),
                               key=operator.itemgetter(1)):
                cbox.addItem(QtGui.QIcon(':/icons/' + v[2]),
                             v[0] + ' (' + k + ')', userData=k)

    def _getCurrencyIndex(self, iso):
        for i, d in enumerate(sorted(currency.Currencies.items(),
                                     key=operator.itemgetter(1))):
            if iso == d[0]:
                return i

        self._log.warning('Currency {iso} not available!'.format(iso=iso))
        return 1

    def _getSourceCurrency(self):
        return self.sourceCombo.itemData(self.sourceCombo.currentIndex())

    def _getTargetCurrency(self):
        return self.targetCombo.itemData(self.targetCombo.currentIndex())

    def _loadConfig(self):
        self.config = config.Config()
        self.config.read()
        value = self.config.source
        self.sourceCombo.setCurrentIndex(self._getCurrencyIndex(value))
        value = self.config.target
        self.targetCombo.setCurrentIndex(self._getCurrencyIndex(value))
        hide = [self.responseLabel1, self.responseLabel2]
        for widget in hide:
            widget.hide()

        if not self.actionCalc.isChecked():
            self.calculator.hide()

    def closeEvent(self, event):
        self.config.source = self._getSourceCurrency()
        self.config.target = self._getTargetCurrency()
        self.config.write()
        QtGui.QMainWindow.closeEvent(self, event)

    def showHelpContents(self):
        "Slot for showing the help contents."""
        msg = 'Implement: <help contents>'
        self._log.debug(msg)

    def showAbout(self):
        """Slot showing the about dialog."""
        pass  # AboutDialog().exec_()

    def clearInput(self):
        """Slot for clearing the input line edit."""
        self.inputValue.setText('')

    def convert(self):
        """Slot for the converting selected currencies."""
        value = self._calculate()
        if not value is None:
            source = self._getSourceCurrency()
            target = self._getTargetCurrency()
            try:
                response, rate = self.converter.convert(source, target, value)
                self.responseLabel1.setText(format(response))
                txtf = 'Exchangerate: {}'
                self.responseLabel2.setText(txtf.format(rate))
                self.responseLabel1.show()
                self.responseLabel2.show()
            except currency.ApiError as e:
                self._log.error(str(e))

    def onInputChanged(self, text):
        pass

    def toggleCalc(self, show):
        """Slot for toggling the calculator widget."""
        if show:
            self.calculator.show()
        else:
            self.calculator.hide()

    def onCalcButtonClicked(self):
        button = self.sender()
        txt = button.text()
        try:
            int(txt)
            value = self.inputValue.text()
            self._updateInputValue(value + txt)
        except ValueError:
            if '=' == txt:
                value = self._calculate()
                if not value is None:
                    self._updateInputValue(value)
            else:
                self._prepareCalculation(txt)

    def _calculate(self):
        """Returns a string corrosponding to the the avaulation of the
        input text buffer. If the evaluation fails, a infomessage is
        displayed, and None is returned.
        """
        expr = self.inputValue.text()
        try:
            return str(eval(expr))
        except Exception as e:
            if len(expr) < 1:
                msg = 'Please enter a valid value to convert!'
                #value = Gtk.MessageType.WARNING
            else:
                msg = 'Error: ' + str(e)
                #value = Gtk.MessageType.ERROR

            #self._set_info_text(msg, value)
            print msg
            return None

    def _prepareCalculation(self, operand):
        """Appends an `operand` to the input line edit."""
        tmp = self.inputValue.text()
        if tmp == '-':
            return
        if tmp == '':
            if operand == '-':
                self._updateInputValue(operand)
        else:
            try:
                int(tmp[-1])
            except ValueError:
                tmp = tmp[:-1]

            self._updateInputValue(tmp + operand)

    def _updateInputValue(self, value):
        """Utility method for updating the input text buffer."""
        self.inputValue.setText(value)


class AboutDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(self)


def main(data):
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName(appInfo.name)
    app.setApplicationName(appInfo.name)
    app.setApplicationVersion(appInfo.version)
    app.setWindowIcon(QtGui.QIcon(':/icons/48/cconverter'))

    win = CConverterQtWindow(data)
    app.lastWindowClosed.connect(win.close)

    win.show()
    sys.exit(app.exec_())
