# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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

import datetime
from promogest.ui.gtk_compat import *
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *
from promogest.dao.Pagamento import Pagamento
from promogest.modules.Pagamenti.dao.TestataDocumentoScadenza import TestataDocumentoScadenza


class PagamentoWidget(GladeWidget):
    __gtype_name__ = 'PagamentoWidget'
    """ Classe wrapper per l'interfaccia della singola scadenza
    """

    label = 'rata generica'

    def __init__(self, owner, label=None):
        GladeWidget.__init__(self, root='pagamento_box',
                             path='Pagamenti/gui/_pagamento_elements.glade',
                             isModule=True)

        if label:
            self.label = label
        self.id_pagamento_scadenza_ccb.connect('clicked',
                                               on_id_pagamento_customcombobox_clicked)
        self.id_banca_scadenza_ccb.connect('clicked',
                                           on_id_banca_customcombobox_clicked)
        self.pulisci_rata_button.connect('clicked',
                                         self.on_pulisci_rata_button_clicked)
        self.data_pagamento_scadenza_entry.entry.connect('changed',
                                                         self.on_data_pagamento_scadenza_entry_changed)
        self.id_pagamento_scadenza_ccb.combobox.connect('changed',
                                                        self.on_id_pagamento_scadenza_ccb_changed)
        fillComboboxPagamenti(self.id_pagamento_scadenza_ccb.combobox)
        fillComboboxBanche(self.id_banca_scadenza_ccb.combobox, short=20)
        self._owner = owner
        self.show_all()

    def fill(self, scadenza):
        """ Riempie i campi con i dati della scadenza
        """
        self.data_scadenza_entry.set_text(dateToString(scadenza.data) or '')
        self.importo_scadenza_entry.set_text(str(scadenza.importo or '0'))
        findComboboxRowFromId(self.id_pagamento_scadenza_ccb.combobox, scadenza.id_pagamento)
        if scadenza.id_banca:
            findComboboxRowFromStr(self.id_banca_scadenza_ccb.combobox, scadenza.id_banca, 1)
        textview_set_text(self.note_scadenza_textview, scadenza.note_per_primanota or '')
        self.data_pagamento_scadenza_entry.set_text(dateToString(scadenza.data_pagamento or ''))

    def get(self):
        """ Ritorna i dati della scadenza
        """
        tds = TestataDocumentoScadenza()
        tds.id_testata_documento = self._owner.dao.id
        tds.data = stringToDate(self.data_scadenza_entry.get_text())
        tds.importo = float(self.importo_scadenza_entry.get_text() or '0')
        tds.id_pagamento = findIdFromCombobox(self.id_pagamento_scadenza_ccb.combobox)
        tds.data_pagamento = stringToDate(self.data_pagamento_scadenza_entry.get_text())
        tds.id_banca = findIdFromCombobox(self.id_banca_scadenza_ccb.combobox)
        tds.note_per_primanota = textview_get_text(self.note_scadenza_textview) or ''
        return tds

    def on_pulisci_rata_button_clicked(self, button):
        """ Pulizia dei campi relativi alla rata
        """
        self.data_scadenza_entry.set_text("")
        self.id_pagamento_scadenza_ccb.combobox.set_active(-1)
        self.id_banca_scadenza_ccb.combobox.set_active(-1)
        self.data_pagamento_scadenza_entry.set_text("")
        self.importo_scadenza_entry.set_text("")
        textview_set_text(self.note_scadenza_textview, "")

    def on_data_pagamento_scadenza_entry_changed(self, entry):
        """ Reimposta i totali saldato e da saldare alla modifica della data
            di pagamento della scadenza """
        self._owner.pagamenti_page.ricalcola_sospeso_e_pagato()

    def on_id_pagamento_scadenza_ccb_changed(self, combobox):
        self._owner.pagamenti_page.ricalcola_sospeso_e_pagato()

    def show_all(self):
        self.data_scadenza_entry.show_all()
        self.id_pagamento_scadenza_ccb.show_all()
        self.id_banca_scadenza_ccb.show_all()
        self.data_pagamento_scadenza_entry.show_all()

    def draw(self):
        """
        Designs results layout
        """
        self._owner.draw()

    def clear(self):
        """ Clears filter's parameters
        """
        self._owner.clear()

    def refresh(self):
        """
        Refresh of results output
        """
        self._owner.refresh()
