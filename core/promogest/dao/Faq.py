# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao

try:
    t_faq=Table('faq', params['metadata'],schema = params['schema'],autoload=True)
except:
    from data.faq import t_faq

class Faq(Dao):

    def __init__(self, req= None,arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == "title":
            dic= { k :t_faq.c.title == v}
        elif k =="active":
            dic= { k :t_faq.c.active == v}
        elif k =="permalink":
            dic= { k :t_faq.c.permalink == v}
        elif k == 'searchkey':
            dic = {k:or_(t_faq.c.title.ilike("%"+v+"%"),
                        t_faq.c.abstract.ilike("%"+v+"%"),
                        t_faq.c.body.ilike("%"+v+"%"))}
        return  dic[k]


std_mapper = mapper(Faq, t_faq, properties={
                }, order_by=t_faq.c.id.desc())
