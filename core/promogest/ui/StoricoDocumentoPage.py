# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2014 by Promotux
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

import sys
import datetime
from promogest.ui.gtk_compat import *
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.modules.Pagamenti.ui import AnagraficadocumentiPagamentExt
from promogest.ui.widgets.PagamentoWidget import PagamentoWidget
from promogest.dao.Pagamento import Pagamento
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.modules.Pagamenti.dao.TestataDocumentoScadenza import TestataDocumentoScadenza
from promogest.lib.HtmlHandler import renderTemplate

if Environment.pg3:
    from gi.repository.WebKit import WebView
    from gi.repository.WebKit import WebSettings
else:
    from webkit import WebView
    from webkit import WebSettings

from promogest.dao.StoricoDocumento import get_padre, get_figli

class StoricoDocumentoPage(GladeWidget):
    """ Widget di configurazione del codice installazione e dei parametri
    di configurazione """
    def __init__(self, mainnn):
        GladeWidget.__init__(self, root='storico_vbox',
                             path='storico_notebook.glade')
        self.ana = mainnn
        self.draw()

    def draw(self):
        # from promogest.dao.StoricoDocumento import StoricoDocumento
        # docs = StoricoDocumento().select(padre=self.ana.dao.id)
        # print "Documento padre", docs
        # docs = StoricoDocumento().select(figli=self.ana.dao.id)
        # print "documenti figli", docs
        self.web_view = WebView()
        self.placeholder_scrolledwindow.add(self.web_view)
        self.web_view.show()
        self.clear()

    def on_mostra_storico_button_clicked(self, widget):
        if self.ana.dao:

            my_page_data = {
                'file': 'storico_documenti.html',
                'padre': get_padre(self.ana.dao.id),
                'figli': get_figli(self.ana.dao.id),
                'dao': self.ana.dao
            }

            html = renderTemplate(pageData=my_page_data)

            self.web_view.load_html_string(html, "file:///"+sys.path[0]+os.sep)


    def clear(self):
        pass
