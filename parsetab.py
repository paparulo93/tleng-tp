
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'firstCOMA CORCHEDER CORCHEIZQ DOSPUNTOS FALSE LLAVEDER LLAVEIZQ NULL NUMBER STRING TRUEfirst : value object : LLAVEIZQ LLAVEDER\n\t\t\t\t| LLAVEIZQ members LLAVEDER members : pair\n\t\t\t\t| pair COMA members pair : STRING DOSPUNTOS valuearray : CORCHEIZQ CORCHEDER\n\t\t\t| CORCHEIZQ elements CORCHEDER elements : value COMA elements\n\t\t\t\t| value value : array value : object value : STRING value : NUMBER value : TRUE value : FALSE value : NULL '
    
_lr_action_items = {'DOSPUNTOS':([17,],[22,]),'COMA':([1,3,4,7,8,9,10,12,13,16,18,20,21,25,],[-11,-13,-14,-15,-12,-17,-16,19,-7,-2,23,-8,-3,-6,]),'STRING':([0,5,11,19,22,23,],[3,3,17,3,3,17,]),'NUMBER':([0,5,19,22,],[4,4,4,4,]),'CORCHEIZQ':([0,5,19,22,],[5,5,5,5,]),'$end':([1,2,3,4,6,7,8,9,10,13,16,20,21,],[-11,0,-13,-14,-1,-15,-12,-17,-16,-7,-2,-8,-3,]),'CORCHEDER':([1,3,4,5,7,8,9,10,12,13,14,16,20,21,24,],[-11,-13,-14,13,-15,-12,-17,-16,-10,-7,20,-2,-8,-3,-9,]),'TRUE':([0,5,19,22,],[7,7,7,7,]),'NULL':([0,5,19,22,],[9,9,9,9,]),'LLAVEDER':([1,3,4,7,8,9,10,11,13,15,16,18,20,21,25,26,],[-11,-13,-14,-15,-12,-17,-16,16,-7,21,-2,-4,-8,-3,-6,-5,]),'FALSE':([0,5,19,22,],[10,10,10,10,]),'LLAVEIZQ':([0,5,19,22,],[11,11,11,11,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'array':([0,5,19,22,],[1,1,1,1,]),'first':([0,],[2,]),'value':([0,5,19,22,],[6,12,12,25,]),'members':([11,23,],[15,26,]),'pair':([11,23,],[18,18,]),'elements':([5,19,],[14,24,]),'object':([0,5,19,22,],[8,8,8,8,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> first","S'",1,None,None,None),
  ('first -> value','first',1,'p_first','tptleng.py',46),
  ('object -> LLAVEIZQ LLAVEDER','object',2,'p_object','tptleng.py',51),
  ('object -> LLAVEIZQ members LLAVEDER','object',3,'p_object','tptleng.py',52),
  ('members -> pair','members',1,'p_members','tptleng.py',62),
  ('members -> pair COMA members','members',3,'p_members','tptleng.py',63),
  ('pair -> STRING DOSPUNTOS value','pair',3,'p_pair','tptleng.py',73),
  ('array -> CORCHEIZQ CORCHEDER','array',2,'p_array','tptleng.py',78),
  ('array -> CORCHEIZQ elements CORCHEDER','array',3,'p_array','tptleng.py',79),
  ('elements -> value COMA elements','elements',3,'p_elements','tptleng.py',89),
  ('elements -> value','elements',1,'p_elements','tptleng.py',90),
  ('value -> array','value',1,'p_value_array','tptleng.py',99),
  ('value -> object','value',1,'p_value_object','tptleng.py',103),
  ('value -> STRING','value',1,'p_value_string','tptleng.py',107),
  ('value -> NUMBER','value',1,'p_value_number','tptleng.py',111),
  ('value -> TRUE','value',1,'p_value_true','tptleng.py',115),
  ('value -> FALSE','value',1,'p_value_false','tptleng.py',119),
  ('value -> NULL','value',1,'p_value_null','tptleng.py',123),
]
