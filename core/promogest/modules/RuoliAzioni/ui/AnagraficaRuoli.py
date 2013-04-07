# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
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

from promogest.ui.AnagraficaSemplice import Anagrafica, AnagraficaDetail, AnagraficaFilter
from promogest import Environment
from promogest.modules.RuoliAzioni.dao.Role import Role
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *
from promogest.ui.gtk_compat import *


class AnagraficaRuoli(Anagrafica):
    """ Anagrafica dei ruoli """

    def __init__(self):
        Anagrafica.__init__(self, 'Promogest - Anagrafica Ruoli',
                            '_Ruoli',
                            AnagraficaRuoliFilter(self),
                            AnagraficaRuoliDetail(self))


    def draw(self):
        self._treeViewModel = self.filter.filter_listore
        self.refresh()


    def refresh(self):
        # Aggiornamento TreeView
        name = prepareFilterString(self.filter.name_filter_entry.get_text())
        self.numRecords = Role().count(name=name)
        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return Role().select(name=name,
                                    orderBy=self.orderBy,
                                    offset=self.offset,
                                    batchSize=self.batchSize)

        self._filterClosure = filterClosure

        cats = self.runFilter()

        self._treeViewModel.clear()

        for c in cats:
            self._treeViewModel.append((c,
                                        (c.name or ''),
                                        (c.descrizione or '')))



class AnagraficaRuoliFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica dei ruoli """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  root='anagrafica_ruoli_filter_table',
                                  path='RuoliAzioni/gui/_anagrafica_ruoli_elements.glade',
                                    isModule=True)
        self._widgetFirstFocus = self.name_filter_entry


    def clear(self):
        # Annullamento filtro
        self.name_filter_entry.set_text('')
        self.name_filter_entry.grab_focus()
        self._anagrafica.refresh()


class AnagraficaRuoliDetail(AnagraficaDetail):
    """ Dettaglio dell'anagrafica dei ruoli """

    def __init__(self, anagrafica):
        AnagraficaDetail.__init__(self,
                                  anagrafica,
                                  path='RuoliAzioni/gui/_anagrafica_ruoli_elements.glade',
                                  isModule=True)


    def setDao(self, dao):
        self.dao = dao
        if dao is None:
            self.dao = Role()
            self._anagrafica._newRow((self.dao, '', ''))
        return self.dao

    def updateDao(self):
        self.dao = Role().getRecord(id=self.dao.id)
        self._refresh()

    def _refresh(self):
        if not self.dao:
            return
        sel = self._anagrafica.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        if not iterator:
            return
        model.set_value(iterator, 0, self.dao)
        model.set_value(iterator, 1, self.dao.name)
        model.set_value(iterator, 2, self.dao.descrizione)

    def saveDao(self):
        sel = self._anagrafica.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()

        name = model.get_value(iterator, 1) or ''
        descrizione = model.get_value(iterator, 2) or ''
        if (name == ''):
            obligatoryField(self._anagrafica.getTopLevel(),
                            self._anagrafica.anagrafica_treeview)
        if (descrizione == ''):
            obligatoryField(self._anagrafica.getTopLevel(),
                            self._anagrafica.anagrafica_treeview)

        self.dao.name = name
        self.dao.descrizione = descrizione
        self.dao.persist()

    def deleteDao(self):
        self.dao.delete()
