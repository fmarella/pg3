#!/usr/local/bin/python
# -*- coding: utf-8 -*-

#    Copyright (C) 2013 by Francesco Marella

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
path = ".."
if path not in sys.path:
    sys.path.append(path)

from sqlachemy import *
import migrate
from promogest import preEnv
preEnv.tipodbforce = "postgresql"
preEnv.aziendaforce = "urbani"
from promogest.Environment import *
from promogest.modules.Pagamenti.dao.TestataDocumentoScadenza import TestataDocumentoScadenza

if __name__ == '__main__':
    kval = {}
    for p in allp:
        kval[p.denominazione] = p.id

    for tds in session.query(TestataDocumentoScadenza).all():
        try:
            tds.id_pagamento = kval[tds.pagamento]
        except:
            tds.id_pagamento = None

    session.flush()

