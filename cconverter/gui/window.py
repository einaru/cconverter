# -*- coding: utf-8 -*-
"""
:Date: Fri Jul 22 16:21:58 CEST 2011
:Authors: Einar Uvsløkk <einar.uvslokk@linux.com>
:Copyright: (c) 2011 Einar Uvsløkk
:License: GNU General Public License (GPL) version 3 or later

vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
"""
from __future__ import division
import logging
import os
import operator

from gettext import gettext as _

import pango
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf

from ..core import currency, config
from ..core import app_info


class CConverterGui:
    """Ebethron currency converter is a simple gtk application for
    converting different currencies to another currency.
    """
    _log = logging.getLogger(__name__)

    def __init__(self, data):
        builder = Gtk.Builder()

        self.data = data
        self.converter = currency.CurrencyConverter()

        filename = os.path.join(data['PKG_DATA_DIR'], 'ui', 'main.glade')
        builder.add_from_file(filename)
        builder.connect_signals(self)

        # Grab and setup widgets we need access to
        self.window = builder.get_object('window')
        actiongroup = builder.get_object('AppActions')
        self.calc_action = actiongroup.get_action('AppCalc')
        accelgroup = Gtk.AccelGroup()
        self.window.add_accel_group(accelgroup)

        for action in actiongroup.list_actions():
            action.set_accel_group(accelgroup)

        toolbar = builder.get_object('toolbar')
        toolbar.get_style_context().add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)

        self.input_value = builder.get_object('input_value')
        self.input_buffer = builder.get_object('input_buffer')
        self.source_combo = builder.get_object('source_combo')
        self.response_label1 = builder.get_object('response_label1')
        self.response_label2 = builder.get_object('response_label2')
        self.target_combo = builder.get_object('target_combo')
        self.convert_button = builder.get_object('convert_button')
        self.equal_button = builder.get_object('button_equal')
        self.calculator = builder.get_object('calculator')

        self._init_comboboxes()

        attr = pango.AttrList()
        attr.insert(pango.AttrSize(30000, 0, -1))
        self.response_label1.set_attributes(attr)
        self._log.debug('Fix new style pango attributes')

        table = builder.get_object('table')
        self.infobar = Gtk.InfoBar()
        self.info = Gtk.Label()
        self.info.set_line_wrap(True)
        self.infobar.get_content_area().pack_start(self.info, True, True, 0)
        self.infobar.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.infobar.connect('response', self._hide_widget)
        table.attach(self.infobar, 0, 1, 1, 2,
                     Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL,
                     0, 0, 0)

        self.window.connect('destroy', self.on_destroy)
        self.window.connect('key-press-event', self.on_keypress_event)
        self.window.set_default_icon_name('cconverter')

    def run(self):
        """Main application entry point."""
        self.window.show_all()
        self.config = config.Config()
        self.config.read()

        value = self.config.source
        self.source_combo.set_active(self._get_currency_index(value))
        msg = 'Setting default source currency: {}'
        self._log.info(msg.format(value))

        value = self.config.target
        self.target_combo.set_active(self._get_currency_index(value))
        msg = 'Setting default target currency: {}'
        self._log.info(msg.format(value))

        value = self.config.api
        self.converter.api = value
        msg = 'Setting default exchangerate source: {}'
        self._log.info(msg.format(value))

        hide = [self.infobar, self.response_label1, self.response_label2]
        for widget in hide:
            self._hide_widget(widget)
            self._log.debug('Hiding widget: {}'.format(widget.get_name()))
        Gtk.main()

    def on_destroy(self, widget=None):
        """Main application exit point."""
        self.config.source = self._get_current_source_currency()
        self.config.target = self._get_current_target_currency()
        self.config.api = self.converter.api
        self.config.write()
        Gtk.main_quit()

    def _set_info_text(self, text, value=2):
        self.info.set_text(text)
        self.infobar.set_message_type(Gtk.MessageType(value))
        self.infobar.show()

    def _init_comboboxes(self):
        """Initialize the comboboxes with the supported currencies,
        which are defined in the currencies module.
        """
        cboxes = [self.source_combo, self.target_combo]
        for cbox in cboxes:
            cbox.set_model(self._get_currency_store())

            renderer = Gtk.CellRendererPixbuf()
            cbox.pack_start(renderer, True)
            cbox.add_attribute(renderer, 'pixbuf', 0)

            renderer = Gtk.CellRendererText()
            cbox.pack_start(renderer, True)
            cbox.add_attribute(renderer, 'text', 1)

            renderer = Gtk.CellRendererText()
            cbox.pack_start(renderer, True)
            cbox.add_attribute(renderer, 'text', 2)

    def _get_flag_icon(self, iso):
        filename = os.path.join(self.data['PKG_DATA_DIR'],
                                'icons', 'flags',
                                '{}.png'.format(iso))
        return GdkPixbuf.Pixbuf.new_from_file(filename)

    def _get_currency_store(self):
        """Initialize the currency dropdown options."""
        store = Gtk.ListStore(GdkPixbuf.Pixbuf, str, str)

        for k, v in sorted(currency.Currencies.items(),
                           key=operator.itemgetter(1)):
            store.append((self._get_flag_icon(v[2]), v[0], k))

        return store

    def _get_currency_index(self, iso):
        """Returns the index to use for `iso` in the comboboxes.

        :param iso: a ISO 4217 currency code.
        :type iso: string
        :rtype: int
        """
        for i, d in enumerate(sorted(currency.Currencies.items(),
                                     key=operator.itemgetter(1))):
            if iso == d[0]:
                return i

        self._log.warning('Currency {iso} not available!'.format(iso=iso))
        return 1

    def _get_current_source_currency(self):
        """Utility method that returns the currently selected currency
        code to convert from.
        """
        model = self.source_combo.get_model()
        iter_from = model.get_iter(self.source_combo.get_active())
        return model.get_value(iter_from, 2)

    def _get_current_target_currency(self):
        """Utility method that returns the currently selected currency
        code to convert to.
        """
        model = self.target_combo.get_model()
        iter_from = model.get_iter(self.target_combo.get_active())
        return model.get_value(iter_from, 2)

    def _hide_widget(self, widget, data=None):
        Gtk.Widget.hide(widget)

    def _show_widget(self, widget, date=None):
        Gtk.Widget.show(widget)

    def on_keypress_event(self, widget, event):
        """Callback for the key-press-event signal.

        Handles all keyboard shortcuts.
        """
        if event.keyval == Gdk.KEY_q:
            if event.state == Gdk.ModifierType.CONTROL_MASK:
                self.on_destroy()
        elif event.keyval == Gdk.KEY_c:
            if event.state == Gdk.ModifierType.CONTROL_MASK:
                self.calc_action.set_active(not self.calc_action.get_active())
        elif event.keyval == Gdk.KEY_Return:
            if event.state == Gdk.ModifierType.CONTROL_MASK:
                self.equal_button.emit('activate')
            else:
                if self.infobar.get_visible():
                    self._hide_widget(self.infobar)
                else:
                    self.convert_button.emit('activate')
        elif event.keyval == Gdk.KEY_F1:
            self.on_help()
        elif event.keyval == Gdk.KEY_F12:
            self.on_about()
        elif event.keyval == Gdk.KEY_Delete:
            self.on_clear()

    def on_edit_preferences(self, widget):
        """Callback for displaying the application preference dialog."""
        dialog = Gtk.Dialog(title=_('Preferences'), parent=self.window,
                            flags=Gtk.DialogFlags.MODAL |
                                  Gtk.DialogFlags.DESTROY_WITH_PARENT,
                            buttons=(Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE))

        content = dialog.get_content_area()

        frame = Gtk.Frame(label=_('<b>Use exchangerates from:</b>'))
        frame.get_label_widget().set_use_markup(True)
        alignment = Gtk.Alignment(xalign=0.5, yalign=0.5, xscale=1, yscale=1)
        alignment.set_properties(left_padding=12)
        table = Gtk.Table(rows=3, columns=2, homogeneous=False)
        table.set_properties(row_spacing=2, column_spacing=2)

        content.pack_start(frame, False, False, 0)
        frame.add(alignment)
        alignment.add(table)

        size = Gtk.IconSize.BUTTON
        attach_opt = Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL
        opt = [('yahoo', 'Yahoo!', 'http://finance.yahoo.com'),
               ('google', 'Google', 'http://www.google.com'),
               ('exchangerate-api', 'Exchangerate Api',
                'http://www.exchangerate-api.com')]
        j = 0
        button = None
        for i in range(len(opt)):
            image = Gtk.Image()
            image.set_from_icon_name(opt[i][0], size)
            button = Gtk.RadioButton(group=button, label=opt[i][1])
            button.set_properties(name=opt[i][0], tooltip_text=opt[i][2])
            if opt[i][0] == self.converter.api:
                button.set_active(True)
            table.attach(image, j, j + 1, i, i + 1, attach_opt, 0, 0, 0)
            table.attach(button, j + 1, j + 2, i, i + 1, attach_opt, 0, 0, 0)

        frame.show_all()

        response = dialog.run()
        if response == Gtk.ResponseType.CLOSE:
            active = [r for r in button.get_group() if r.get_active()][0]
            if active.get_name() != self.converter.api:
                self.converter.api = active.get_name()

        dialog.destroy()

    def on_help(self, widget=None):
        """Callback for the help action."""
        self._log.debug('NotImplemented <on_help>')

    def on_about(self, widget=None):
        """Callback for the about action."""
        about = Gtk.AboutDialog(title=_('About'), parent=self.window,
                              flags=Gtk.DialogFlags.MODAL |
                                    Gtk.DialogFlags.DESTROY_WITH_PARENT)
        about.set_program_name(app_info.name)
        about.set_version(app_info.version)
        about.set_comments(app_info.description)
        about.set_copyright(app_info.copyright)
        about.set_website(app_info.website)
        about.set_authors(app_info.authors)
        about.set_logo_icon_name('cconverter')
        about.set_license(app_info.license)
        about.set_wrap_license(True)
        about.connect('response', lambda a, b: Gtk.Widget.destroy(a))
        about.show()

    def on_clear(self, widget=None):
        """Callback for the clear action."""
        self.input_buffer.set_text('', -1)

    def on_input_changed(self, widget=None):
        """Callback for the changed signal in the value input entry."""
        pass

    def on_convert(self, widget=None):
        """Callback for the convert action."""
        value = self._calculate()
        if not value is None:
            original = self._get_current_source_currency()
            target = self._get_current_target_currency()
            try:
                result, rate = self.converter.convert(original, target, value)
                self.response_label1.set_text(format(result))
                self.response_label2.set_text('Exhangerate: {}'.format(rate))
                self._show_widget(self.response_label1)
                self._show_widget(self.response_label2)
            except currency.ApiError as e:
                value = Gtk.MessageType.ERROR
                self._set_info_text(format(e), value)
                self._log.error(format(e))

    def on_calc_toggled(self, widget):
        """Callback for the calculator toggle action."""
        self.calculator.set_visible(widget.get_active())

    def on_calc_button_activate(self, widget):
        """Callback for the various buttons in the calculator widget."""
        txt = widget.get_label()
        try:
            int(txt)
            value = self.input_buffer.get_text()
            self._update_buffer_value(value + txt)
        except ValueError:
            if txt == '=':
                value = self._calculate()
                if not value is None:
                    self._update_buffer_value(value)
            else:
                self._prepare_calculation(txt)

    def _calculate(self):
        """Returns a string corrosponding to the the avaulation of the
        input text buffer. If the evaluation fails, a infomessage is
        displayed, and None is returned.
        """
        expr = self.input_buffer.get_text()
        try:
            return str(eval(expr))
        except Exception as e:
            if len(expr) < 1:
                msg = 'Please enter a valid value to convert!'
                value = Gtk.MessageType.WARNING
            else:
                msg = format(e)
                value = Gtk.MessageType.ERROR

            self._set_info_text(msg, value)
            return None

    def _prepare_calculation(self, operand):
        """Appends an `operand` to the input text buffer."""
        tmp = self.input_value.get_text()

        if tmp == '':
            if operand == '-':
                self._update_buffer_value(operand)
        else:
            try:
                int(tmp[-1])
            except ValueError:
                tmp = tmp[:-1]

            self._update_buffer_value(tmp + operand)

    def _update_buffer_value(self, text):
        """Utility method for updating the input text buffer."""
        self.input_buffer.set_text(text, len(text))
        self.input_value.grab_focus()
        self.input_value.set_position(len(text))


def register_stock_icons(config):
    """Enable icon theming for the application."""
    iconsdir = os.path.join(config['PKG_DATA_DIR'], 'icons',)
    icontheme = Gtk.IconTheme.get_default()
    icontheme.append_search_path(iconsdir)


def main(config):
    register_stock_icons(config)
    CConverterGui(config).run()
