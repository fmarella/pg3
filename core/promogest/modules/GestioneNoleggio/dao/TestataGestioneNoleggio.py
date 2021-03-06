# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni <francesco@promotux.it>

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

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao


try:
    testatadocumentonoleggio = Table('testata_documento_noleggio', params['metadata'],
                                schema = params['schema'], autoload=True)
except:
    testataDocumento=Table('testata_documento', params['metadata'],schema = params['schema'],autoload=True)

    if tipodb == "sqlite":
        testatadocumentoFK = 'testata_documento.id'
    else:
        testatadocumentoFK = params['schema']+'.testata_documento.id'

    testatadocumentonoleggio = Table('testata_documento_noleggio', params['metadata'],
                        Column('id',Integer,primary_key=True),
                        Column('id_testata_documento',Integer,ForeignKey(testatadocumentoFK,onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
                        Column('data_inizio_noleggio',DateTime, nullable=False),
                        Column('data_fine_noleggio',DateTime,nullable=False),
                        schema=params['schema'])
    testatadocumentonoleggio.create(checkfirst=True)


class TestataGestioneNoleggio(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'id':
            dic= {k:testatadocumentonoleggio.c.id ==v}
        elif k == 'idTestataDocumento':
            dic= {k:testatadocumentonoleggio.c.id_testata_documento==v}
        elif k == 'daData':
            dic = {k :testatadocumentonoleggio.c.data_inizio_noleggio >= v}
        elif k == 'aData':
            dic = {k:testatadocumentonoleggio.c.data_inizio_noleggio <= v}
        return  dic[k]

std_mapper = mapper(TestataGestioneNoleggio, testatadocumentonoleggio,properties={
        }, order_by=testatadocumentonoleggio.c.id)
