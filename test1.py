#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: andrey
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import soapy



class test1(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "test1")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################

        self.soapy_sdrplay_source_0 = None
        _agc_setpoint = int((-30))
        _agc_setpoint = max(min(_agc_setpoint, -20), -70)

        dev = 'driver=sdrplay'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        def _set_soapy_sdrplay_source_0_gain_mode(channel, agc):
            self.soapy_sdrplay_source_0.set_gain_mode(channel, agc)
            if not agc:
                self.set_soapy_sdrplay_source_0_gain(channel, self._soapy_sdrplay_source_0_gain_value)
        self.set_soapy_sdrplay_source_0_gain_mode = _set_soapy_sdrplay_source_0_gain_mode
        self._soapy_sdrplay_source_0_gain_value = 20

        def _set_soapy_sdrplay_source_0_gain(channel, gain):
            self._soapy_sdrplay_source_0_gain_value = gain
            if not self.soapy_sdrplay_source_0.get_gain_mode(channel):
                self.soapy_sdrplay_source_0.set_gain(channel, 'IFGR', min(max(59 - gain, 20), 59))
        self.set_soapy_sdrplay_source_0_gain = _set_soapy_sdrplay_source_0_gain

        def _set_soapy_sdrplay_source_0_lna_state(channel, lna_state):
                self.soapy_sdrplay_source_0.set_gain(channel, 'RFGR', min(max(lna_state, 0), 9))
        self.set_soapy_sdrplay_source_0_lna_state = _set_soapy_sdrplay_source_0_lna_state

        self.soapy_sdrplay_source_0 = soapy.source(dev, "fc32", 1, 'driver=sdrplay',
                                  stream_args, tune_args, settings)
        self.soapy_sdrplay_source_0.set_sample_rate(0, 3000000)
        self.soapy_sdrplay_source_0.set_bandwidth(0, 5000000)
        self.soapy_sdrplay_source_0.set_antenna(0, 'RX')
        self.soapy_sdrplay_source_0.set_frequency(0, 85000000)
        self.soapy_sdrplay_source_0.set_frequency_correction(0, 0)
        # biasT_ctrl is not always available and leaving it blank avoids errors
        if '' != '':
            self.soapy_sdrplay_source_0.write_setting('biasT_ctrl', )
        self.soapy_sdrplay_source_0.write_setting('agc_setpoint', (-30))
        self.set_soapy_sdrplay_source_0_gain_mode(0, False)
        self.set_soapy_sdrplay_source_0_gain(0, 20)
        self.set_soapy_sdrplay_source_0_lna_state(0, 3)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                3000000,
                2000000000,
                300000,
                window.WIN_HAMMING,
                6.76))
        self.blocks_probe_signal_x_0 = blocks.probe_signal_c()


        ##################################################
        # Connections
        ##################################################
        self.connect((self.low_pass_filter_0, 0), (self.blocks_probe_signal_x_0, 0))
        self.connect((self.soapy_sdrplay_source_0, 0), (self.low_pass_filter_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "test1")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate




def main(top_block_cls=test1, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
