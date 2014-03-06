# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012
#    by Promotux di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@anche.no>

#    This file is part of Promogest.

#    Promogest is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.

#    Promogest is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Promogest.  If not, see <http://www.gnu.org/licenses/>.

from promogest.dao.Magazzino import Magazzino
from promogest import Environment
from promogest.ui.utilsCombobox import fillComboboxCCardType
from promogest.lib.utils import setconf


def drawPart(anag):
    accelGroup = Gtk.AccelGroup()
    anag.getTopLevel().add_accel_group(accelGroup)
    anag.contanti_radio_button.add_accelerator('clicked', accelGroup,
                                        Gdk.KEY_F1, 0, Gtk.AccelFlags.VISIBLE)
    anag.assegni_radio_button.add_accelerator('clicked', accelGroup,
                                        Gdk.KEY_F2, 0, Gtk.AccelFlags.VISIBLE)
    anag.carta_di_credito_radio_button.add_accelerator('clicked', accelGroup,
                                        Gdk.KEY_F3, 0, Gtk.AccelFlags.VISIBLE)
    anag.total_button.add_accelerator('grab_focus', accelGroup,
                                        Gdk.KEY_F5, 0, Gtk.AccelFlags.VISIBLE)
    anag.total_button.set_focus_on_click(False)

    # Costruisco treeview scontrino
    anag.modelRiga = Gtk.ListStore(int, str, str, str, str,
                                            str, str, str, str, str,str,str,str)

    treeview = anag.scontrino_treeview
    rendererSx = Gtk.CellRendererText()
    rendererDx = Gtk.CellRendererText()
    rendererDx.set_property('xalign', 1)

    anag.lsmodel = Gtk.ListStore(int, str)
    cellcombo1= Gtk.CellRendererCombo()
    cellcombo1.set_property("editable", True)
    cellcombo1.set_property("visible", True)
    cellcombo1.set_property("text-column", 1)
    cellcombo1.set_property("editable", True)
    cellcombo1.set_property("has-entry", False)
    cellcombo1.set_property("model", anag.lsmodel)
    cellcombo1.connect('edited', anag.on_column_listinoRiga_edited,
                                                            treeview, True)
    column = Gtk.TreeViewColumn('List.', cellcombo1, text=1, background=10,font=11)
    column.set_sizing(Gtk.TreeViewColumnSizing.GROW_ONLY)
    column.set_clickable(True)
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(20)
    treeview.append_column(column)

    column = Gtk.TreeViewColumn('Codice a barre', rendererSx, text=2,background=10,font=11)
    column.set_sizing(Gtk.TreeViewColumnSizing.GROW_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(90)
    treeview.append_column(column)

    column = Gtk.TreeViewColumn('Codice', rendererSx, text=3, background=10,font=11)
    column.set_sizing(Gtk.TreeViewColumnSizing.GROW_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(70)
    treeview.append_column(column)

    cellrendererDescrizione = Gtk.CellRendererText()
    cellrendererDescrizione.set_property("editable", True)
    cellrendererDescrizione.set_property("visible", True)
    cellrendererDescrizione.connect('edited',
                        anag.on_column_descrizione_edited, treeview, True)
    column = Gtk.TreeViewColumn('Descrizione', cellrendererDescrizione, text=4,background=10, font=11)
    column.set_sizing(Gtk.TreeViewColumnSizing.GROW_ONLY)
    column.set_clickable(True)
    rendererSx.connect('edited', anag.on_column_descrizione_edited,
                                                            treeview, True)
    column.set_resizable(True)
    column.set_expand(True)
    column.set_min_width(50)
    treeview.append_column(column)

    cellspin = Gtk.CellRendererSpin()
    cellspin.set_property("editable", True)
    cellspin.set_property("visible", True)
    adjustment = Gtk.Adjustment(1, 1, 1000, 0.500, 2)
    cellspin.set_property("adjustment", adjustment)
    cellspin.set_property("digits", 3)
    cellspin.set_property("climb-rate", 3)
    #cellspin.set_property("foreground", "orange")

    cellspin.connect('edited', anag.on_column_prezzo_edited, treeview, True)
    column = Gtk.TreeViewColumn('Prezzo', cellspin, text=5, background=10, font=11)
    column.set_sizing(Gtk.TreeViewColumnSizing.GROW_ONLY)
    #column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(80)
    treeview.append_column(column)

    cellspinsconto = Gtk.CellRendererSpin()
    cellspinsconto.set_property("editable", True)
    cellspinsconto.set_property("visible", True)
    adjustment = Gtk.Adjustment(1, 1, 1000, 1, 2)
    cellspinsconto.set_property("adjustment", adjustment)
    #cellspin.set_property("digits",3)
    #cellspin.set_property("climb-rate",3)
    cellspinsconto.connect('edited', anag.on_column_sconto_edited,
                                                            treeview, True)
    column = Gtk.TreeViewColumn('Sconto', cellspinsconto, text=6,background=10,font=11)
    column.set_sizing(Gtk.TreeViewColumnSizing.GROW_ONLY)
    column.set_clickable(True)
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(50)
    treeview.append_column(column)


    lsmodel = Gtk.ListStore(str)
    lsmodel.append(["%"])
    lsmodel.append(["€"])
    cellcombo= Gtk.CellRendererCombo()
    cellcombo.set_property("editable", True)
    cellcombo.set_property("visible", True)
    cellcombo.set_property("text-column", 0)
    cellcombo.set_property("editable", True)
    cellcombo.set_property("has-entry", False)
    cellcombo.set_property("model", lsmodel)
    cellcombo.connect('edited', anag.on_column_tipo_edited, treeview, True)
    column = Gtk.TreeViewColumn('Tipo', cellcombo, text=7,background=10,font=11)
    column.set_sizing(Gtk.TreeViewColumnSizing.GROW_ONLY)
    column.set_clickable(True)
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(20)
    treeview.append_column(column)

    column = Gtk.TreeViewColumn('Pr.Scont', rendererDx, text=8,background=10,font=11)
    column.set_sizing(Gtk.TreeViewColumnSizing.GROW_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(50)
    treeview.append_column(column)

    cellspin = Gtk.CellRendererSpin()
    cellspin.set_property("editable", True)
    cellspin.set_property("visible", True)
    adjustment = Gtk.Adjustment(1, 1, 1000, 1, 2)
    cellspin.set_property("adjustment", adjustment)
    cellspin.set_property("digits", 2)
    cellspin.set_property("climb-rate", 3)
    cellspin.connect('edited', anag.on_column_quantita_edited, treeview, True)
    column = Gtk.TreeViewColumn('Quantità', cellspin, text=9,background=10,font=11)
    column.set_sizing(Gtk.TreeViewColumnSizing.GROW_ONLY)
    #column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(50)
    treeview.append_column(column)

    column = Gtk.TreeViewColumn('Totale', rendererSx, text=12, background=10,font=11)
    column.set_sizing(Gtk.TreeViewColumnSizing.GROW_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(70)
    treeview.append_column(column)


    treeview.set_model(anag.modelRiga)

    # Disabilito bottoni e text entry
    #anag.confirm_button.set_sensitive(False)
    anag.delete_button.set_sensitive(False)
    anag.rhesus_button.set_sensitive(False)
    #anag.annulling_button.set_sensitive(False)
    anag.total_button.set_sensitive(False)
    anag.subtotal_button.set_sensitive(False)
    anag.empty_button.set_sensitive(False)
    anag.sconto_hbox.set_sensitive(False)
    anag.setPagamento(enabled = False)

    anag.codice_a_barre_entry.grab_focus()
    anag._loading = False

    # Segnali
    treeViewSelection = anag.scontrino_treeview.get_selection()
    anag.scontrino_treeview.set_property('rules-hint', True)
    treeViewSelection.connect('changed',
                            anag.on_scontrino_treeview_selection_changed)
    fillComboboxCCardType(anag.card_type_combobox)
    # Ricerca listino
    anag.id_listino = anag.ricercaListino()

    # Ricerca magazzino
    if hasattr(Environment.conf, "VenditaDettaglio"):
        magalist = Magazzino().select(denominazione = Environment.conf.VenditaDettaglio.magazzino,
                                    offset = None,
                                    batchSize = None)
        if len(magalist) > 0:
            anag.id_magazzino = magalist[0].id
        else:
            anag.id_magazzino = None
    else:
        anag.id_magazzino = setconf("VenditaDettaglio", "magazzino_vendita")

    # Vado in stato di ricerca
    anag._state = 'search'
    anag.empty_current_row()
