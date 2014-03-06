# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
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

from gi.repository import Gtk, Gdk
from CustomComboBoxSearch import CustomComboBoxSearch
from promogest.lib.utils import leggiFornitore, findIdFromCombobox


class FornitoreSearchWidget(CustomComboBoxSearch):
    """ Classe base per la ricerca fornitori """
    __gtype_name__ = 'FornitoreSearchWidget'

    def __init__(self):
        CustomComboBoxSearch.__init__(self)

        self.connect('changed',
                           self.on_entry_key_press_event)

        self.connect("destroy-event", self.on_widget_destroy)
        self.connect("icon-press", self.on_icon_press)
        self._callName = None
        self._ricerca = None
        self._filter = True
        self._resultsCount = 0
        self.clear()


    def on_icon_press(self,entry,position,event):
        """
        scopettina agganciata ad un segnale generico
        """
        if position.value_nick == "primary":

            def refresh_entry(anagWindow):
                self._resultsCount = self._ricerca.getResultsCount()
                resultsElement = self._ricerca.getResultsElement()
                if not(self._resultsCount > 0):
                    self.set_active(0)
                    return

                if self._resultsCount == 1:
                    id = resultsElement.id
                    res = leggiFornitore(id)
                    denominazione = res["ragioneSociale"]
                    if denominazione == '':
                        denominazione = res["nome"] + ' ' + res["cognome"]
                    self.set_text(denominazione)
                    self._id = id
                    #self.on_completion_match_main()
            from promogest.ui.RicercaComplessaFornitori import RicercaComplessaFornitori
            try:
                idCat = findIdFromCombobox(self.anaedit.
                id_categoria_fornitore_customcombobox.combobox)
            except:
                idCat = None
            self._ricerca = RicercaComplessaFornitori(idCategoria = idCat)
            if not self._filter:
                self._ricerca.setTreeViewSelectionType(Gtk.SelectionMode.SINGLE)
            else:
                self._ricerca.refresh()
            anagWindow = self._ricerca.getTopLevel()
            returnWindow = self.get_toplevel()
            anagWindow.set_transient_for(returnWindow)
            anagWindow.connect("hide",
                               refresh_entry)
            self._ricerca.show_all()

        else:                            #secondary
             self.clear_entry()

    def ricercaDao(self, keyname):
        from promogest.dao.Fornitore import Fornitore
        try:
            idCat = findIdFromCombobox(self.anaedit.
            id_categoria_fornitore_customcombobox.combobox)
        except:
            idCat = None
        cli = Fornitore().select(ragioneSociale=keyname,idCategoria=idCat, batchSize=40)
        model = self.completion.get_model()
        model.clear()
        for m in cli:
            model.append(('empty', m.id, m.ragione_sociale, m))


    def setId(self, value):
        self.insertComboboxSearchFornitore(self, value)

    def getId(self):
        #if self.isEmpty():
            #self.clear()
        #elif (self._resultsCount > 1) and (self._ricerca is not None):
            #self._ricerca.refresh()
            #return self.idlist
        return self._id

    def getData(self):
        return self._container

    def insertComboboxSearchFornitore(self, combobox, idFornitore, clear=False, filter=True):
        res = leggiFornitore(idFornitore)
        denominazione = res["ragioneSociale"]
        if denominazione == '':
            denominazione = res["nome"] + ' ' + res["cognome"]
        combobox.refresh(idFornitore, denominazione, res, clear, filter)

    def clear(self):
        self.set_active(0)

    def setOnChangedCall(self, callName=None):
        self._callName = callName

    def setSingleValue(self):
        self._filter = False

    def setMultipleValues(self):
        self._filter = True

    def on_widget_destroy(self, widget, event):
        if self._ricerca is not None:
            anagWindow = self._ricerca.getTopLevel()
            anagWindow.destroy()
            del self._ricerca
            self._ricerca = None
