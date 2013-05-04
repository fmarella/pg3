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
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *
from promogest import Environment
from promogest.Environment import session
from promogest.ui.GladeWidget import GladeWidget
from promogest.modules.Pagamenti.ui import AnagraficadocumentiPagamentExt
from promogest.dao.Pagamento import Pagamento
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.modules.Pagamenti.dao.TestataDocumentoScadenza import TestataDocumentoScadenza


class PagamentiNotebookPage(GladeWidget):
    """ Widget di configurazione del codice installazione e dei parametri
    di configurazione """
    def __init__(self, mainnn):
        GladeWidget.__init__(self, root='pagamenti_vbox',
                             path='Pagamenti/gui/pagamenti_notebook.glade',
                             isModule=True)
        self.ana = mainnn
        scadenza_model = None
#        # lista di scadenze
#        self.rate = []
#        # assegno un'istanza di PagamentoWidget se ho un acconto, None altrimenti
#        self.acconto = None
        self.draw()

    def draw(self):
        fillComboboxPagamenti(self.id_pagamento_customcombobox.combobox)
        self.id_pagamento_customcombobox.connect('clicked',
            on_id_pagamento_customcombobox_clicked)
        self.id_pagamento_customcombobox.combobox.connect('changed',
            self.id_pagamento_customcombobox_changed)
        fillComboboxBanche(self.id_banca_customcombobox.combobox)
        self.id_banca_customcombobox.connect('clicked',
            on_id_banca_customcombobox_clicked)

        # inizializza la pagina con i widget delle scadenze
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

        self.clear()

    def id_pagamento_customcombobox_changed(self, combobox):
        if self.ana._loading:
            return
        self.on_calcola_importi_scadenza_button_clicked(None)

    def on_apri_primanota_clicked(self, widget):
        from promogest.modules.PrimaNota.ui.AnagraficaPrimaNota import AnagraficaPrimaNota
        anag = AnagraficaPrimaNota(aziendaStr=Environment.azienda)
        win = anag.getTopLevel()
        win.set_transient_for(self.ana.dialogTopLevel)
        anag.show_all()

    def on_primanota_check_toggled(self, widget):
        pass

    def clear(self):
        '''
        '''
        self.id_pagamento_customcombobox.combobox.set_active(-1)
        val = Decimal(self.ana.totale_scontato_riepiloghi_label.get_text() or 0)
        self.totale_in_pagamenti_label.set_markup('<b><span foreground="black" size="24000">'+str(mN(val, 2))+'</span></b>')
        self.totale_pagato_scadenza_label.set_markup('<b><span foreground="#338000" size="24000">0</span></b>')
        self.totale_sospeso_scadenza_label.set_markup('<b><span foreground="#B40000" size="24000">0</span></b>')
        self.stato_label.set_markup('<b><span foreground="#B40000" size="24000">'+_('APERTO')+'</span></b>')
        self.metodo_pagamento_label.set_markup('<b><span foreground="black" size="16000">'+_("NESSUNO?")+'</span></b>')
        self.importo_primo_documento_entry.set_text('')
        self.importo_secondo_documento_entry.set_text('')
        self.numero_primo_documento_entry.set_text('')
        self.numero_secondo_documento_entry.set_text('')
        self.primanota_check.set_active(True)
#        if self.acconto:
#            self.acconto_scheda_togglebutton.set_active(False)
#        if len(self.rate) > 0:
#            for i in self.rate:
#                self.scadenze_notebook.remove_page(0)
#            self.rate = []
#            # devono essere rimosse tutta una serie di dati collegati alle scadenze
#            # come ad esempio prima nota
#            self.ana.dao.testataDocumentoScadenzaDel()

#    def on_aggiungi_rate_button_clicked(self, button):
#        '''
#        '''
#        numero = len(self.rate) + 1
#        pag_w = PagamentoWidget(self.ana, 'rata ' + str(numero))
#        self.rate.append(pag_w)
#        self.scadenze_notebook.insert_page(pag_w.getTopLevel(), gtk.Label(pag_w.label), -1)
#        self.scadenze_notebook.set_current_page(-1)

#    def on_rimuovi_rate_button_clicked(self, button):
#        ''' Elimina una scheda di pagamento e la relativa rata
#        '''
#        if len(self.rate) > 0:
#            if YesNoDialog(msg=_('Rimuovere la rata?\n\nAlcune informazioni andranno perse per sempre.')):
#                scadenza = self.rate.pop()
#                #TODO: rimuovere la scadenza da testata_documento_scadenza
#                #scadenza.get_model().delete()
#
#                self.scadenze_notebook.remove_page(-1)
#        else:
#            messageInfo('Non ci sono altre scadenze da rimuovere.')

    def on_aggiorna_pagamenti_button_clicked(self, button):
        """
        Aggiorna la parte dei pagamenti
        """
        self.ricalcola_sospeso_e_pagato()

    def on_seleziona_prima_nota_button_clicked(self, button):
        """
        Seleziona la prima nota da utilizzare come riferimento
        """
        if self.numero_primo_documento_entry.get_text() != "":
            response = self.impostaDocumentoCollegato(int(self.numero_primo_documento_entry.get_text()))
        else:
            messageInfo(msg="Inserisci il numero del documento")
            response = False

        if response:
            self.importo_primo_documento_entry.set_text(str(response))
            self.dividi_importo()
            self.ricalcola_sospeso_e_pagato()
            self.numero_secondo_documento_entry.set_sensitive(True)
            self.seleziona_seconda_nota_button.set_sensitive(True)
            self.importo_secondo_documento_entry.set_sensitive(True)

    def on_seleziona_seconda_nota_button_clicked(self, button):
        if self.numero_secondo_documento_entry.get_text() != "":
            response = self.impostaDocumentoCollegato(int(self.numero_secondo_documento_entry.get_text()))
        else:
            messageInfo(msg="Inserisci il numero del documento")
            response = False
        if response:
            self.importo_primo_documento_entry.set_text(str(response))
            self.dividi_importo()
            self.ricalcola_sospeso_e_pagato()


    def impostaDocumentoCollegato(self, numerodocumento):
        """
        Imposta il documento indicato dall'utente come collegato al documento
        in creazione.
        """

        documento = AnagraficadocumentiPagamentExt.getDocumentoCollegato(self.ana, numerodocumento)
        if documento is None:
            return False
        daoTestata = TestataDocumento().getRecord(id=documento.id)
        tipo_documento = daoTestata.operazione
        totale_pagato = daoTestata.totale_pagato
        totale_sospeso = daoTestata.totale_sospeso
        numero_documento = daoTestata.numero
        data_documento = daoTestata.data_documento

        if totale_sospeso != 0:
            messageError(msg="""Attenzione. Risulta che il documento da Lei scelto abbia ancora
un importo in sospeso. Il documento, per poter essere collegato, deve essere completamente saldato""")
            return False

        return totale_pagato

    def on_calcola_importi_scadenza_button_clicked(self, button):
        """
        Calcola importi scadenza pagamenti
        """
        id_pag = findIdFromCombobox(self.id_pagamento_customcombobox.combobox)
        if id_pag == -1 or id_pag==0 or id_pag==None:
            messageInfo(msg=_("NESSUN METODO DI PAGAMENTO SELEZIONATO\n NON POSSO AGIRE"))
            return
        pago = Pagamento().getRecord(id=id_pag)
        if pago:
            self.metodo_pagamento_label.set_markup('<b><span foreground="black" size="16000">'+str(pago.denominazione)+'</span></b>')
            val = Decimal(self.ana.totale_scontato_riepiloghi_label.get_text() or 0) + Decimal(str(self.calcola_spese()))
            self.totale_in_pagamenti_label.set_markup('<b><span foreground="black" size="24000">'+str(mN(val, 2))+'</span></b>')
        else:
            self.metodo_pagamento_label.set_markup('<b><span foreground="black" size="16000">'+str(_("NESSUNO?"))+'</span></b>')
            val = Decimal(self.ana.totale_scontato_riepiloghi_label.get_text() or 0)
            self.totale_in_pagamenti_label.set_markup('<b><span foreground="black" size="24000">'+str(mN(val, 2))+'</span></b>')
        if self.ana.dao.documento_saldato:
            msg = _('Attenzione! Stai per riaprire un documento già saldato.\n Continuare ?')
            if YesNoDialog(msg=msg, transient=self.ana.dialogTopLevel):
                self.stato_label.set_markup('<b><span foreground="#B40000" size="24000">'+_('APERTO')+'</span></b>')
            else:
                return
        res = self.attiva_scadenze()
        if not res:
            return
        self.dividi_importo()
        self.ricalcola_sospeso_e_pagato()

    def on_chiudi_pagamento_documento_button_clicked(self, button):
        """
        Chiude un pagamento
        """
        acconto = 0
        importo_immesso = 0
        for rata in self.rate:
            daoTDS = rata.get_model()
            importo_immesso += daoTDS.importo

        if self.acconto:
            daoAcconto = self.acconto.get_model()
            acconto = daoAcconto.importo

        if acconto == 0 or importo_immesso == 0 or importo_immesso < float(self.totale_in_pagamenti_label.get_text()):
            msg = _('Chiusura di un documento con pagamenti nulli o parziali.\n Continuare?')
            if YesNoDialog(msg=msg, transient=None):
                self.stato_label.set_markup('<b><span foreground="#338000" size="24000">'+_('PAGATO')+'</span></b>')
                self.chiudi_pagamento_documento_button.set_sensitive(False)
                self.apri_pagamento_documento_button.set_sensitive(True)
        else:
            self.stato_label.set_markup('<b><span foreground="#338000" size="24000">'+_('PAGATO')+'</span></b>')

    def on_apri_pagamento_documento_button_clicked(self, button):
        ''' Apre il pagamento
        '''
        msg=_('Attenzione! Stai per riaprire un documento considerato già pagato.\n Continuare?')
        if YesNoDialog(msg=msg):
            self.stato_label.set_markup('<b><span foreground="#B40000" size="24000">'+_('APERTO')+'</span></b>')
            self.apri_pagamento_documento_button.set_sensitive(False)
            self.chiudi_pagamento_documento_button.set_sensitive(True)

#    def on_acconto_scheda_togglebutton_toggled(self, button):
#        """
#
#        """
#        if not self.acconto:
#            self.acconto_scheda_togglebutton.set_label(_('Acconto'))
#            self.acconto = PagamentoWidget(self.ana, 'Acconto')
#            dao = self.acconto.get_model()
#            dao.data = datetime.datetime.now()
#            self.acconto.set_model(dao)
#            self.scadenze_notebook.insert_page(self.acconto.getTopLevel(), gtk.Label(self.acconto.label), 0)
#            self.scadenze_notebook.set_current_page(0)
#        else:
#            self.acconto_scheda_togglebutton.set_label(_('Acconto'))
#            self.scadenze_notebook.remove_page(0)
#            self.scadenze_notebook.set_current_page(-1)
#            self.acconto = None

#    def on_pulisci_scadenza_button_clicked(self, button):
#        """
#        Pulisce tutti i campi relativi alla scheda pagamenti
#        """
#        msg = _('Stai per rimuovere i riferimenti già inseriti. Continuare?')
#        if YesNoDialog(msg=msg):
#            self.clear()
#            self.ricalcola_sospeso_e_pagato()

    # INIZIO GESTIONE SCADENZE

    def __clear_scadenza(self):
        self.scadenza_model = None
        self.data_scadenza_entry.set_text("")
        self.id_pagamento_scadenza_ccb.combobox.set_active(-1)
        self.id_banca_scadenza_ccb.combobox.set_active(-1)
        self.data_pagamento_scadenza_entry.set_text("")
        self.importo_scadenza_entry.set_text("0")
        textview_set_text(self.note_scadenza_textview, "")

    def __load_scadenze(self):
        self.scadenze_liststore.clear()
        for tds in self.ana.dao.testata_documento_scadenza:
            self.scadenze_liststore.append([tds, tds.numero_scadenza, "data scadenza: %s\n  importo %s" % (dateToString(tds.data), tds.importo)])

    def on_scadenze_treeview_cursor_changed(self, treeview):
        sel = treeview.get_selection()
        (model, iterator) = sel.get_selected()
        if iterator:
            scadenza = model.get_value(iterator, 0)
            self.data_scadenza_entry.set_text(dateToString(scadenza.data) or '')
            self.importo_scadenza_entry.set_text(str(scadenza.importo or '0'))
            if scadenza.id_pagamento:
                findComboboxRowFromId(self.id_pagamento_scadenza_ccb.combobox,
                                      scadenza.id_pagamento)
            if scadenza.id_banca:
                findComboboxRowFromStr(self.id_banca_scadenza_ccb.combobox,
                                       scadenza.id_banca, 1)
            textview_set_text(self.note_scadenza_textview, scadenza.note_per_primanota or '')
            self.data_pagamento_scadenza_entry.set_text(dateToString(scadenza.data_pagamento or ''))
            self.scadenza_model = scadenza
            self.save_button.set_sensitive(True)
            self.revert_button.set_sensitive(True)

    def on_new_scadenza_button_clicked(self, button):
        self.__clear_scadenza()
        self.save_button.set_sensitive(True)
        self.revert_button.set_sensitive(True)
        self.scadenza_model = TestataDocumentoScadenza()
        self.scadenza_model.id_testata_documento = self.ana.dao.id
        num = 0
        for tds in self.ana.dao.testata_documento_scadenza:
            if tds.numero_scadenza > num:
                num = tds.numero_scadenza
        self.scadenza_model.numero_scadenza = num + 1
        self.data_scadenza_entry.grab_focus()

    def on_remove_scadenza_button_clicked(self, button):
        self.ana.dao.primanota_del_all()
        self.scadenza_model.delete()
        session.commit()
        self.__clear_scadenza()
        self.__load_scadenze()

    def on_revert_button_clicked(self, button):
        self.__clear_scadenza()
        self.save_button.set_sensitive(False)
        button.set_sensitive(False)

    def on_save_button_clicked(self, button):
        self.ana.dao.primanota_del_all()
        self.scadenza_model.data = stringToDate(self.data_scadenza_entry.get_text())
        self.scadenza_model.importo = float(self.importo_scadenza_entry.get_text() or '0')
        self.scadenza_model.id_pagamento = findIdFromCombobox(self.id_pagamento_scadenza_ccb.combobox)
        self.scadenza_model.data_pagamento = stringToDate(self.data_pagamento_scadenza_entry.get_text())
        self.scadenza_model.id_banca = findIdFromCombobox(self.id_banca_scadenza_ccb.combobox)
        self.scadenza_model.note_per_primanota = textview_get_text(self.note_scadenza_textview) or ''
        session.add(self.scadenza_model)
        session.commit()
        self.save_button.set_sensitive(False)
        self.revert_button.set_sensitive(False)
        self.__clear_scadenza()
        self.__load_scadenze()

    def on_controlla_rate_scadenza_button_clicked(self, button):
        """ bottone che controlla le rate scadenza """
        self.controlla_rate_scadenza(self, True)

    def on_pulisci_rata_button_clicked(self, button):
        """ Pulizia dei campi relativi alla rata
        """
        self.__clear_scadenza()

    def on_data_pagamento_scadenza_entry_changed(self, entry):
        """ Reimposta i totali saldato e da saldare alla modifica della data
            di pagamento della scadenza """
        self.ricalcola_sospeso_e_pagato()

    def on_id_pagamento_scadenza_ccb_changed(self, combobox):
        self.ricalcola_sospeso_e_pagato()
    # FINE GESTIONE SCADENZE

    def getScadenze(self):
        if self.ana.dao.testata_documento_scadenza:
            self.__load_scadenze()

            if self.ana.dao.ripartire_importo is None:
                self.ana.dao.ripartire_importo = True
            self.primanota_check.set_active(self.ana.dao.ripartire_importo)
            if not self.ana.dao.ripartire_importo:
                msg="""Eventuali pagamenti inseriti in Prima Nota andranno persi.
\nControlla l\'opzione "<b>Inserisci pagamenti in prima nota cassa</b>" nella scheda Pagamenti."""
                messageWarning(msg=msg)

            if self.ana.dao.documento_saldato:
                self.stato_label.set_markup('<b><span foreground="#338000" size="24000">'+_('PAGATO')+'</span></b>')
            else:
                self.stato_label.set_markup('<b><span foreground="#B40000" size="24000">'+_('APERTO')+'</span></b>')
            self.totale_pagato_scadenza_label.set_markup('<b><span foreground="#338000" size="24000">'+str(
                mN(self.ana.dao.totale_pagato) or 0)+'</span></b>')

            if (self.ana.dao.totale_sospeso is None)  or (self.ana.dao.totale_sospeso == 0):
                totaleSospeso = Decimal(str(self.ana.totale_scontato_riepiloghi_label.get_text() or 0)) - Decimal(str(self.ana.dao.totale_pagato or 0))
            else:
                totaleSospeso = self.ana.dao.totale_sospeso

            self.totale_sospeso_scadenza_label.set_markup('<b><span foreground="#B40000" size="24000">'+str(
                mN(totaleSospeso))+'</span></b>')
            if self.ana.dao.id_primo_riferimento != None:
                doc = TestataDocumento().getRecord(id=self.ana.dao.id_primo_riferimento)
                self.importo_primo_documento_entry.set_text(str(doc.totale_pagato) or '')
                self.numero_primo_documento_entry.set_text(str(doc.numero) or '')
                self.importo_secondo_documento_entry.set_sensitive(True)
                self.numero_secondo_documento_entry.set_sensitive(True)
                self.seleziona_seconda_nota_button.set_sensitive(True)
                if self.ana.dao.id_secondo_riferimento != None:
                    doc = TestataDocumento().getRecord(id=self.ana.dao.id_secondo_riferimento)
                    self.importo_secondo_documento_entry.set_text(str(doc.totale_pagato) or '')
                    self.numero_secondo_documento_entry.set_text(str(doc.numero) or '')
                else:
                    self.importo_secondo_documento_entry.set_text('')
                    self.numero_secondo_documento_entry.set_text('')
            else:
                self.importo_primo_documento_entry.set_text('')
                self.importo_secondo_documento_entry.set_text('')
                self.numero_primo_documento_entry.set_text('')
                self.numero_secondo_documento_entry.set_text('')

    def saveScadenze(self):
        ''' Gestione del salvataggio dei dati di pagamento
        '''
        print "CHECKKKK saveScadenze"
        #TODO: aggiungere la cancellazione se vengono trovate più righe?
        self.ana.dao.totale_pagato = float(self.totale_pagato_scadenza_label.get_text())
        self.ana.dao.totale_sospeso = float(self.totale_sospeso_scadenza_label.get_text())
        if self.stato_label.get_text() == "PAGATO":
            self.ana.dao.documento_saldato = True
        else:
            self.ana.dao.documento_saldato = False
        self.ana.dao.ripartire_importo =  self.primanota_check.get_active()
        #scadenze = []

#        if self.acconto:
#            daoTestataDocumentoScadenza = self.acconto.get_model()
#            daoTestataDocumentoScadenza.id_testata_documento = self.ana.dao.id
#            daoTestataDocumentoScadenza.numero_scadenza = 0
#            if not daoTestataDocumentoScadenza.importo:
#                daoTestataDocumentoScadenza.importo = Decimal(0)
#            if not daoTestataDocumentoScadenza.pagamento:
#                daoTestataDocumentoScadenza.pagamento = 'n/a'
#            if not daoTestataDocumentoScadenza.data:
#                daoTestataDocumentoScadenza.data = datetime.datetime.now()
#            daoTestataDocumentoScadenza.data_pagamento = daoTestataDocumentoScadenza.data
#            #scadenze.append(daoTestataDocumentoScadenza)
#            Environment.session.add(daoTestataDocumentoScadenza)
#        i = 1
#        for rata in self.rate:
#            daoTestataDocumentoScadenza = rata.get_model()
#            daoTestataDocumentoScadenza.id_testata_documento = self.ana.dao.id
#            daoTestataDocumentoScadenza.numero_scadenza = i
#            if not daoTestataDocumentoScadenza.importo:
#                daoTestataDocumentoScadenza.importo = Decimal(0)
#            if not daoTestataDocumentoScadenza.pagamento:
#                daoTestataDocumentoScadenza.pagamento = 'n/a'
#            if not daoTestataDocumentoScadenza.data:
#                daoTestataDocumentoScadenza.data = datetime.datetime.now()
#            if controllaDateFestivi(daoTestataDocumentoScadenza.data):
#                daoTestataDocumentoScadenza.data = daoTestataDocumentoScadenza.data + datetime.timedelta(5)
#            Environment.session.add(daoTestataDocumentoScadenza)
#            i += 1
#            #scadenze.append(daoTestataDocumentoScadenza)
#
#        Environment.session.commit()

#        self.ana.dao.testata_documento_scadenza = scadenze
        for s in self.ana.dao.testata_documento_scadenza:
            print "data={0}\nimport={1}\npagamento={2}\nid testata doc={3}\nnumero scadenza={4}".format(s.data,s.importo,s.id_pagamento,s.id_testata_documento, s.numero_scadenza)

        #TODO: finire di sistemare questa parte ......

        doc = self.numero_primo_documento_entry.get_text()
        if doc != "" and doc != "0":
            documentocollegato = AnagraficadocumentiPagamentExt.getDocumentoCollegato(self.ana, int(doc))
            if documentocollegato is not None:
                self.ana.dao.id_primo_riferimento = documentocollegato.id
                doc2 = self.numero_secondo_documento_entry.get_text()
                if doc2 != "" and doc2 != "0":
                    documentocollegato = AnagraficadocumentiPagamentExt.getDocumentoCollegato(self.ana, int(doc2))
                    if documentocollegato is not None:
                        self.ana.dao.id_secondo_riferimento = documentocollegato.id

    def attiva_scadenze(self):
        sel = findStrFromCombobox(self.id_pagamento_customcombobox.combobox, 2)
        scadenze = AnagraficadocumentiPagamentExt.IsPagamentoMultiplo(sel)
        data_doc = stringToDate(self.ana.data_documento_entry.get_text())
        importotot = float(self.totale_in_pagamenti_label.get_text() or 0)

        if type(scadenze) == list:
            numeroscadenze = (len(scadenze) - 1) / 2
        else:
            numeroscadenze = 1

        if scadenze[len(scadenze)-1] != "FM":
            fine_mese = False
        else:
            fine_mese = True

        # Rimuovo le rate in eccesso e le relative tabs dall'interfaccia
        y = len(self.rate) - numeroscadenze
        if y > 0:
            msg = 'Rimuovere ' + ngettext('%s rata', '%s rate', y) % y #@UndefinedVariable
            msg += ' dai pagamenti?\n\n Alcune informazioni andranno perse per sempre.'
            if not YesNoDialog(msg=msg):
                return False
            for i in range(abs(y)):
                self.rate.pop()
                self.scadenze_notebook.remove_page(-1)

        # Aggiungo le rate necessarie per il tipo di pagamento scelto
        i = 1
        for j in range(numeroscadenze):
            daoTDS = None
            try:
                daoTDS = self.rate[j].get_model()
            except IndexError:
                daoTDS = TestataDocumentoScadenza()
                daoTDS.id_testata_documento = self.ana.dao.id
            idpag = findIdFromCombobox(self.id_pagamento_customcombobox.combobox)
            if idpag:
                p = Pagamento().getRecord(id=idpag)
                daoTDS.pagamento = p.denominazione
            if type(scadenze) == list:
                daoTDS.data = dateToString(getScadenza(data_doc, int(scadenze[i]), fine_mese))
                i += 2
            else:
                daoTDS.data = data_doc
            try:
                self.rate[j].set_model(daoTDS)
            except IndexError:
                self.on_aggiungi_rate_button_clicked(None)
                self.rate[-1].set_model(daoTDS)
        return True

    def dividi_importo(self):
        """ Divide l'importo passato per il numero delle scadenze. Se viene passato un argomento, che indica
        il valore di una rata, ricalcola gli altri tenendo conto del valore modificato
        TODO: Passare i valori valuta a mN
        """
        importodoc = float(float(self.ana.totale_scontato_riepiloghi_label.get_text() or 0) + self.calcola_spese())
        if importodoc == float(0):
            return
        self.totale_in_pagamenti_label.set_markup('<b><span foreground="black" size="24000">'+str(mN(importodoc, 2))+'</span></b>')

        acconto = float(0)
        if self.acconto:
            daoAcconto = self.acconto.get_model()
            acconto = float(daoAcconto.importo or 0)

        importo_primo_doc = float(self.importo_primo_documento_entry.get_text() or 0)
        importo_secondo_doc = float(self.importo_secondo_documento_entry.get_text() or 0)
        importotot = importodoc - acconto - importo_primo_doc - importo_secondo_doc

        sel = findStrFromCombobox(self.id_pagamento_customcombobox.combobox, 2)
        pagamenti = AnagraficadocumentiPagamentExt.IsPagamentoMultiplo(sel)
        importorate = None
        if type(pagamenti) == list:
            n_pagamenti = (len(pagamenti) - 1) / 2
            importorate = dividi_in_rate(importotot, n_pagamenti)
        else:
            n_pagamenti = 1
            importorate = importotot

#        i = 0
#        for rata in self.rate:
#            daoTDS = rata.get_model()
#            if type(importorate) == list:
#                daoTDS.importo = importorate[i]
#                i += 1
#            else:
#                daoTDS.importo = importorate
#            rata.set_model(daoTDS)

        #TODO: mostrare o nascondere l'acconto ?


    def calcola_spese(self):
        """
        Calcola le spese dei pagamenti
        """
        def getSpesePagamento(pagamento):
            p = Pagamento().select(denominazione=pagamento)
            if len(p) > 0:
                p = p[0]
                if float(p.spese or 0) != float(0):
                    return calcolaPrezzoIva(float(p.spese), float(p.perc_aliquota_iva))
                else:
                    return float(0)
            else:
                return float(0)

        if not self.ana.dao:
            return float(0)
        if not self.ana.dao.id or not self.ana.dao.id_cliente:
            return float(0)
        if self.ana.dao.esclusione_spese == True:
            return float(0)
        spese = float(0)
        # Controllo l'acconto e le rate
#        if self.acconto:
#            dao = self.acconto.get_model()
#            spese += getSpesePagamento(dao.pagamento)
#        if len(self.rate) > 0:
#            for rata in self.rate:
#                dao = rata.get_model()
#                spese += getSpesePagamento(dao.pagamento)
        return spese

    def on_esclusione_spese_checkbutton_toggled(self, widget):
        if self.ana._loading:
            return
        self.ana.dao.esclusione_spese = widget.get_active()
        self.ricalcola_sospeso_e_pagato()

    def controlla_rate_scadenza(self, messaggio):
        """
        Controlla che gli importi inseriti nelle scadenze siano corrispondenti
        al totale del documento. Ritorna False se c'e` un errore,
        True se e` tutto corretto.
        """

        importotot = float(float(self.ana.totale_scontato_riepiloghi_label.get_text() or 0) + self.calcola_spese())
        if importotot == float(0):
            return

        importo_immesso = float(0)
        for rata in self.rate:
            daoTDS = rata.get_model()
            importo_immesso += daoTDS.importo

        if self.acconto:
            daoAcconto = self.acconto.get_model()
            importo_immesso += daoAcconto.importo

        importo_primo_riferimento = float(self.ana.importo_primo_documento_entry.get_text() or 0)
        importo_secondo_riferimento = float(self.ana.importo_secondo_documento_entry.get_text() or 0)

        differenza_importi = (importo_immesso + importo_primo_riferimento +
            importo_secondo_riferimento) - importotot
        if differenza_importi == - importotot:
            if messaggio:
                messageInfo(msg="Importo delle rate non inserite")
            return True

        elif differenza_importi != float(0):
            if messaggio:
                messageInfo(msg="""ATTENZIONE!
La somma degli importi che Lei ha inserito come rate nelle scadenze
non corrisponde al totale del documento. La invitiamo a ricontrollare.
Ricordiamo inoltre che allo stato attuale e` impossibile salvare il documento.
Per l'esattezza, l'errore e` di %.2f""" % differenza_importi)
            return False
        else:
            if messaggio:
                messageInfo(msg="Gli importi inseriti come rate corrispondono con il totale del documento")
            return True

    def ricalcola_sospeso_e_pagato(self):
        """ Reimposta i totali saldato e da saldare alla modifica della data di pagamento
            della quarta scadenza
            Ricalcola i totali sospeso e pagato in base alle
            scadenze ancora da saldare
        """
        spese = self.calcola_spese()
        totale_in_pagamenti_label = float(float(self.ana.totale_scontato_riepiloghi_label.get_text() or 0) + spese)
        self.totale_in_pagamenti_label.set_markup('<b><span foreground="black" size="24000">'+str(mN(totale_in_pagamenti_label, 2))+'</span></b>')
        self.ana.totale_spese_label.set_text(str(mN(spese, 2)))

        acconto = float(0)
#        if self.acconto:
#            daoAcconto = self.acconto.get_model()
#            acconto = daoAcconto.importo

        totalepagato = acconto
        totalesospeso = float(0)

#        for rata in self.rate:
#            daoTDS = rata.get_model()
#            if daoTDS.data_pagamento:
#                totalepagato += daoTDS.importo
#            else:
#                totalesospeso += daoTDS.importo

        totalepagato += float(self.importo_primo_documento_entry.get_text() or '0')
        totalepagato += float(self.importo_secondo_documento_entry.get_text() or '0')

        if totalepagato == float(0):
            totalesospeso = totale_in_pagamenti_label
        if totalesospeso == float(0):
            totalesospeso = totale_in_pagamenti_label - totalepagato

        if totalesospeso > float(0) and not self.ana.dao.documento_saldato:
            self.stato_label.set_markup('<b><span foreground="#B40000" size="24000">'+_('APERTO')+'</span></b>')

        self.totale_pagato_scadenza_label.set_markup('<b><span foreground="#338000" size="24000">'+str(mN(totalepagato, 2))+'</span></b>')
        self.totale_sospeso_scadenza_label.set_markup('<b><span foreground="#B40000" size="24000">'+str(mN(totalesospeso, 2))+'</span></b>')

        if totalepagato == float(0) and totalesospeso == float(0):
            self.stato_label.set_markup('<b><span foreground="#B40000" size="24000">'+_('APERTO')+'</span></b>')

        # se il totale è zero, esci senza proporre la chiusura
        if str(totale_in_pagamenti_label) == '0.0':
            return

        if str(totalepagato) == str(totale_in_pagamenti_label) and \
                        self.stato_label.get_text() == "APERTO" and \
                        self.ana.notebook.get_current_page() == 3:
            msg = """Attenzione! L'importo in sospeso è pari a 0 e
l'importo pagato è uguale al totale documento.
Procedere con la "chiusura" del Pagamento?"""
            if YesNoDialog(msg=msg, transient=None):
                self.stato_label.set_markup('<b><span foreground="#338000" size="24000">'+_('PAGATO')+'</span></b>')
                self.chiudi_pagamento_documento_button.set_sensitive(False)
                self.apri_pagamento_documento_button.set_sensitive(True)
