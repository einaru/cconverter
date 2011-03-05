# -*- coding: utf-8 -*-
#
# gtk.cconverter_gtk
#
# Copyright (c) 2010, 2011
#      Einar Uvsløkk, <einaru@stud.ntnu.no>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/
import sys

from core.currency import currencies, convert
from core.app_info import author, copyright, description
from core.app_info import name, version, website

try:
    import pygtk
    pygtk.require("2.0")
    import gtk
    import gobject
except:
    sys.exit(1)

class CConverterGui:
    """
    Ebethron currency converter is a simple gtk application for converting
    different currencies to another currency
    """

    def __init__(self):
        x = gtk.Builder()
        #x.add_from_file("gui/currency.glade")
        x.add_from_string(glade_ui)
        x.connect_signals(self)

        # Grad the widgets from the widget tree
        self.from_cur_label = x.get_object("from_cur_label")
        self.to_cur_label = x.get_object("to_cur_label")
        self.from_cur_input = x.get_object("from_cur_input")
        self.to_cur_res = x.get_object("to_cur_res")
        self.from_cbox = x.get_object("from_cbox")
        self.to_cbox = x.get_object("to_cbox")
        self.convert = x.get_object("convert")
        self.about = x.get_object("about")
        self.aboutdialog = x.get_object("aboutdialog")
        self.statusbar = x.get_object("statusbar")
        self.win = x.get_object("window")

        # Initialize the comboxes
        self.init_comboboxes()
        self.from_cbox.set_name("from")
        self.from_cbox.set_active(32)   # Defaults to US Dollars
        self.to_cbox.set_name("to")
        self.to_cbox.set_active(22)     # Defaults to Norwegian Krone

        # No local method signal connections
        self.win.connect("destroy", lambda w: gtk.main_quit())
        
        # And finally show the gui
        #self.win.set_icon()
        self.win.show()

    def init_comboboxes(self):
        """
        Initialize the comboboxes with the supported currencies, which are 
        defined in the currencies module
        """
        cboxes = [self.from_cbox, self.to_cbox]
        for cbox in cboxes:
            cbox.set_model(self.get_currency_model())
            cell = gtk.CellRendererText()
            cbox.pack_start(cell, True)
            cbox.add_attribute(cell, 'text', 0)

    def init_about_dialog(self):
        self.aboutdialog.set_program_name(name)
        self.aboutdialog.set_version(version)
        self.aboutdialog.set_comments(description)
        self.aboutdialog.set_copyright(copyright)
        self.aboutdialog.set_website(website)
        self.aboutdialog.set_authors(author)
        self.aboutdialog.run()
        self.aboutdialog.destroy()

    def get_currency_model(self):
        """
        Initialize the currency dropdown options
        """
        model = gtk.ListStore(
            gobject.TYPE_STRING)
        for k, _ in sorted(currencies.items()):
            model.append([k])

        return model

    def _validate_numeric_input(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def on_combobox_changed(self, w):
        """
        Update the currency labels when the combobox selections change
        """
        cur = (currencies[w.get_active_text()])
        if w.get_name() == "from":
            self.from_cur_label.set_text(cur)
        elif w.get_name() == "to":
            self.to_cur_label.set_text(cur)

    def on_convert(self, w):
        """
        Signal handler for the convert button
        """
        if self._validate_numeric_input(self.from_cur_input.get_text()):
            self.statusbar.pop(0)
            result = convert(currencies[self.from_cbox.get_active_text()],
                             currencies[self.to_cbox.get_active_text()],
                             self.from_cur_input.get_text())
            self.to_cur_res.set_text(result)
        else:
            self.statusbar.push(0, "Invalid input! Must be numeric...")

    def on_about(self, w):
        self.aboutdialog.set_program_name(name)
        self.aboutdialog.set_version(version)
        self.aboutdialog.set_comments(description)
        self.aboutdialog.set_copyright(copyright)
        self.aboutdialog.set_website(website)
        self.aboutdialog.set_authors(author)
        self.aboutdialog.run()
        self.aboutdialog.destroy()

def main():
    CConverterGui()
    gtk.main()

glade_ui="""
<?xml version="1.0"?>
<interface>
  <requires lib="gtk+" version="2.16"/>
  <!-- interface-naming-policy project-wide -->
  <object class="GtkWindow" id="window">
    <property name="events">GDK_KEY_PRESS_MASK | GDK_STRUCTURE_MASK</property>
    <property name="title" translatable="yes">Currency Converter</property>
    <property name="window_position">center</property>
    <property name="default_width">300</property>
    <child>
      <object class="GtkVBox" id="vbox1">
        <property name="visible">True</property>
        <property name="orientation">vertical</property>
        <child>
          <object class="GtkAlignment" id="alignment1">
            <property name="visible">True</property>
            <property name="top_padding">5</property>
            <property name="left_padding">5</property>
            <property name="right_padding">5</property>
            <child>
              <object class="GtkVBox" id="vbox2">
                <property name="visible">True</property>
                <property name="orientation">vertical</property>
                <child>
                  <object class="GtkViewport" id="viewport1">
                    <property name="visible">True</property>
                    <property name="resize_mode">queue</property>
                    <property name="shadow_type">etched-in</property>
                    <child>
                      <object class="GtkAlignment" id="alignment2">
                        <property name="visible">True</property>
                        <property name="top_padding">5</property>
                        <property name="bottom_padding">5</property>
                        <property name="left_padding">5</property>
                        <property name="right_padding">5</property>
                        <child>
                          <object class="GtkTable" id="table1">
                            <property name="visible">True</property>
                            <property name="n_rows">4</property>
                            <property name="n_columns">2</property>
                            <child>
                              <object class="GtkLabel" id="label1">
                                <property name="visible">True</property>
                                <property name="xalign">0</property>
                                <property name="label" translatable="yes">From</property>
                              </object>
                              <packing>
                                <property name="y_options">GTK_FILL</property>
                                <property name="x_padding">10</property>
                              </packing>
                            </child>
                            <child>
                              <object class="GtkLabel" id="label2">
                                <property name="visible">True</property>
                                <property name="xalign">0</property>
                                <property name="label" translatable="yes">To</property>
                              </object>
                              <packing>
                                <property name="top_attach">1</property>
                                <property name="bottom_attach">2</property>
                                <property name="y_options">GTK_FILL</property>
                                <property name="x_padding">10</property>
                              </packing>
                            </child>
                            <child>
                              <object class="GtkLabel" id="from_cur_label">
                                <property name="visible">True</property>
                                <property name="xalign">0</property>
                                <property name="label" translatable="yes">?</property>
                              </object>
                              <packing>
                                <property name="top_attach">2</property>
                                <property name="bottom_attach">3</property>
                                <property name="y_options">GTK_FILL</property>
                                <property name="x_padding">10</property>
                              </packing>
                            </child>
                            <child>
                              <object class="GtkLabel" id="to_cur_label">
                                <property name="visible">True</property>
                                <property name="xalign">0</property>
                                <property name="label" translatable="yes">?</property>
                              </object>
                              <packing>
                                <property name="top_attach">3</property>
                                <property name="bottom_attach">4</property>
                                <property name="y_options">GTK_FILL</property>
                                <property name="x_padding">10</property>
                              </packing>
                            </child>
                            <child>
                              <object class="GtkComboBox" id="from_cbox">
                                <property name="visible">True</property>
                                <signal name="changed" handler="on_combobox_changed"/>
                              </object>
                              <packing>
                                <property name="left_attach">1</property>
                                <property name="right_attach">2</property>
                                <property name="y_options">GTK_FILL</property>
                              </packing>
                            </child>
                            <child>
                              <object class="GtkComboBox" id="to_cbox">
                                <property name="visible">True</property>
                                <signal name="changed" handler="on_combobox_changed"/>
                              </object>
                              <packing>
                                <property name="left_attach">1</property>
                                <property name="right_attach">2</property>
                                <property name="top_attach">1</property>
                                <property name="bottom_attach">2</property>
                                <property name="y_options">GTK_FILL</property>
                              </packing>
                            </child>
                            <child>
                              <object class="GtkEntry" id="from_cur_input">
                                <property name="visible">True</property>
                                <property name="can_focus">True</property>
                                <property name="has_focus">True</property>
                                <property name="invisible_char">&#x25CF;</property>
                              </object>
                              <packing>
                                <property name="left_attach">1</property>
                                <property name="right_attach">2</property>
                                <property name="top_attach">2</property>
                                <property name="bottom_attach">3</property>
                                <property name="y_options">GTK_FILL</property>
                              </packing>
                            </child>
                            <child>
                              <object class="GtkEntry" id="to_cur_res">
                                <property name="visible">True</property>
                                <property name="can_focus">True</property>
                                <property name="editable">False</property>
                                <property name="invisible_char">&#x25CF;</property>
                              </object>
                              <packing>
                                <property name="left_attach">1</property>
                                <property name="right_attach">2</property>
                                <property name="top_attach">3</property>
                                <property name="bottom_attach">4</property>
                                <property name="y_options">GTK_FILL</property>
                              </packing>
                            </child>
                          </object>
                        </child>
                      </object>
                    </child>
                  </object>
                  <packing>
                    <property name="position">0</property>
                  </packing>
                </child>
                <child>
                  <object class="GtkHButtonBox" id="hbuttonbox1">
                    <property name="visible">True</property>
                    <property name="layout_style">end</property>
                    <child>
                      <object class="GtkButton" id="convert">
                        <property name="label" translatable="yes">_Convert</property>
                        <property name="visible">True</property>
                        <property name="can_focus">True</property>
                        <property name="receives_default">True</property>
                        <property name="use_underline">True</property>
                        <accelerator key="Return" signal="clicked"/>
                        <signal name="clicked" handler="on_convert"/>
                      </object>
                      <packing>
                        <property name="expand">False</property>
                        <property name="fill">False</property>
                        <property name="position">0</property>
                      </packing>
                    </child>
                    <child>
                      <object class="GtkButton" id="about">
                        <property name="label">gtk-about</property>
                        <property name="visible">True</property>
                        <property name="can_focus">True</property>
                        <property name="receives_default">True</property>
                        <property name="use_stock">True</property>
                        <signal name="clicked" handler="on_about"/>
                      </object>
                      <packing>
                        <property name="expand">False</property>
                        <property name="fill">False</property>
                        <property name="position">1</property>
                        <property name="secondary">True</property>
                      </packing>
                    </child>
                  </object>
                  <packing>
                    <property name="expand">False</property>
                    <property name="padding">5</property>
                    <property name="position">1</property>
                  </packing>
                </child>
              </object>
            </child>
          </object>
          <packing>
            <property name="position">0</property>
          </packing>
        </child>
        <child>
          <object class="GtkStatusbar" id="statusbar">
            <property name="visible">True</property>
            <property name="spacing">2</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="position">1</property>
          </packing>
        </child>
      </object>
    </child>
  </object>
  <object class="GtkAboutDialog" id="aboutdialog">
    <property name="border_width">5</property>
    <property name="window_position">center</property>
    <property name="icon_name">emblem-favorite</property>
    <property name="type_hint">normal</property>
    <child internal-child="vbox">
      <object class="GtkVBox" id="dialog-vbox2">
        <property name="visible">True</property>
        <property name="orientation">vertical</property>
        <property name="spacing">2</property>
        <child>
          <placeholder/>
        </child>
        <child internal-child="action_area">
          <object class="GtkHButtonBox" id="dialog-action_area2">
            <property name="visible">True</property>
            <property name="layout_style">end</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="pack_type">end</property>
            <property name="position">0</property>
          </packing>
        </child>
      </object>
    </child>
  </object>
</interface>
"""