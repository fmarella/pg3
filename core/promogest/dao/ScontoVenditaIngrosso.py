# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

#    Author: Pinna Marco (Dr_astico) <zoccolodignu@gmail.com>
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

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *

try:
    t_sconti_vendita_ingrosso = Table('sconti_vendita_ingrosso',
                                  params['metadata'],
                                  schema=params['schema'],
                                  autoload=True)
except:
    from data.scontiVenditaIngrosso import t_sconti_vendita_ingrosso

from Dao import Dao
from Sconto import t_sconto


class ScontoVenditaIngrosso(Dao):
    """  """
    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        if k == 'idListino':
            dic = {k: t_sconti_vendita_ingrosso.c.id_listino==v}
        elif k == 'idArticolo':
            dic = {k: t_sconti_vendita_ingrosso.c.id_articolo==v}
        elif k == 'dataListinoArticolo':
            dic = {k: t_sconti_vendita_ingrosso.c.data_listino_articolo==v}
        return dic[k]

std_mapper = mapper(ScontoVenditaIngrosso,
    join(t_sconto, t_sconti_vendita_ingrosso),
    properties={
        "id": [t_sconto.c.id, t_sconti_vendita_ingrosso.c.id]
    },
    order_by=t_sconti_vendita_ingrosso.c.id)

if tipodb=="sqlite":
    from promogest.dao.Listino import Listino
    a = session.query(Listino.data_listino).all()
    b = session.query(ScontoVenditaIngrosso.data_listino_articolo).all()
    fixit =  list(set(b)-set(a))
    print "fixt-sv-ing", fixit
    for f in fixit:
        if f[0] != "None" and f[0] != None:
            aa = ScontoVenditaIngrosso().select(dataListinoArticolo=f[0], batchSize=None)
            for a in aa:
                session.delete(a)
                session.commit
