# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
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

from promogest.ui.AnagraficaComplessaFilter import AnagraficaFilter
from promogest.modules.Provvigione.dao.Provvigione import Provvigione
from promogest.modules.Provvigione.dao.ProvvPgAzArt import ProvvPgAzArt
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *


class AnagraficaProvvFilter(AnagraficaFilter):
    """ Filtro per la ricerca nei file """

    def __init__(self, anagrafica, daoFrom=None, tipo="Cliente"):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  root='anagrafica_provv_filter_table',
                                  path='Provvigione/gui/_anagrafica_provv_elements.glade',
                                  isModule=True)
        self._widgetFirstFocus = self.denominazione_filter_entry
        self.daoFrom = daoFrom
        self.tipo = tipo

    def draw(self):
        """ """
        self.refresh()

    #def _reOrderBy(self, column):
        #if column.get_name() == "numero":
            #return self._changeOrderBy(column,(None,GestioneFile.numero))
        #if column.get_name() == "data_inizio":
            #return self._changeOrderBy(column,(None,TestataPrimaNota.data_inizio))

    def clear(self):
        self.denominazione_filter_entry.set_text('')
        self.refresh()

    def refresh(self):
        # Aggiornamento TreeView
        #deno = prepareFilterString(self.denominazione_filter_entry.get_text())
        deno = ""

        def filterCountClosure():
            return ProvvPgAzArt().count(
                        id_persona_giuridica_from = self.daoFrom.id,
                        )
        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()
        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return ProvvPgAzArt().select(
                            id_persona_giuridica_from = self.daoFrom.id,
                            offset=offset,
                            batchSize=batchSize)

        self._filterClosure = filterClosure

        valis = self.runFilter()

        self.anagrafica_provv_filter_listore.clear()
        valore = 0
        for i in valis:
#            print i.__dict__
            if i.arti:
                art = i.arti.denominazione
            else:
                art = "TUTTI"
            self.anagrafica_provv_filter_listore.append((i,
                                                        str(mN(i.provv.valore_provv,1)),
                                                        str(i.provv.tipo_provv),
                                                        str(art),
                                                        str(i.pg_from.ragione_sociale),
                                                        str(i.pg_to.ragione_sociale),

#                                                        str(i.arti.denominazione or ""),
                                                        ))
