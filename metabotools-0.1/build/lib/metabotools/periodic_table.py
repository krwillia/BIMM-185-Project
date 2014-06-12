import sys
from collections import namedtuple
import re

test_config = [['C', 'Carbon', 12, 1], ['H', 'Hydrogen', 1, 1], ['O', 'Oxygen', 16, 1], ['N', 'Nitrogen', 14, 1]]

pt_config_average = [
['H', 'Hydrogen', 1.0079, 1],
['He', 'Helium', 4.0026, 1],
['Li', 'Lithium', 6.941, 1],
['Be', 'Beryllium', 9.0122, 1],
['B', 'Boron', 10.811, 1],
['C', 'Carbon', 12.0107, 1],
['N', 'Nitrogen', 14.0067, 1],
['O', 'Oxygen', 15.9994, 1],
['F', 'Fluorine', 18.9984, 1],
['Ne', 'Neon', 20.1797, 1],
['Na', 'Sodium', 22.9897, 1],
['Mg', 'Magnesium', 24.305, 1],
['Al', 'Aluminum', 26.9815, 1],
['Si', 'Silicon', 28.0855, 1],
['P', 'Phosphorus', 30.9738, 1],
['S', 'Sulfur', 32.065, 1],
['Cl', 'Chlorine', 35.453, 1],
['Ar', 'Argon', 39.948, 1],
['K', 'Potassium', 39.0983, 1],
['Ca', 'Calcium', 40.078, 1],
['Sc', 'Scandium', 44.9559, 1],
['Ti', 'Titanium', 47.867, 1],
['V', 'Vanadium', 50.9415, 1],
['Cr', 'Chromium', 51.9961, 1],
['Mn', 'Manganese', 54.938, 1],
['Fe', 'Iron', 55.845, 1],
['Co', 'Cobalt', 58.9332, 1],
['Ni', 'Nickel', 58.6934, 1],
['Cu', 'Copper', 63.546, 1],
['Zn', 'Zinc', 65.39, 1],
['Ga', 'Gallium', 69.723, 1],
['Ge', 'Germanium', 72.64, 1],
['As', 'Arsenic', 74.9216, 1],
['Se', 'Selenium', 78.96, 1],
['Br', 'Bromine', 79.904, 1],
['Kr', 'Krypton', 83.8, 1],
['Rb', 'Rubidium', 85.4678, 1],
['Sr', 'Strontium', 87.62, 1],
['Y', 'Yttrium', 88.9059, 1],
['Zr', 'Zirconium', 91.224, 1],
['Nb', 'Niobium', 92.9064, 1],
['Mo', 'Molybdenum', 95.94, 1],
['Tc', 'Technetium', 98.0, 1],
['Ru', 'Ruthenium', 101.07, 1],
['Rh', 'Rhodium', 102.9055, 1],
['Pd', 'Palladium', 106.42, 1],
['Ag', 'Silver', 107.8682, 1],
['Cd', 'Cadmium', 112.411, 1],
['In', 'Indium', 114.818, 1],
['Sn', 'Tin', 118.71, 1],
['Sb', 'Antimony', 121.76, 1],
['Te', 'Tellurium', 127.6, 1],
['I', 'Iodine', 126.9045, 1],
['Xe', 'Xenon', 131.293, 1],
['Cs', 'Cesium', 132.9055, 1],
['Ba', 'Barium', 137.327, 1],
['La', 'Lanthanum', 138.9055, 1],
['Ce', 'Cerium', 140.116, 1],
['Pr', 'Praseodymium', 140.9077, 1],
['Nd', 'Neodymium', 144.24, 1],
['Pm', 'Promethium', 145.0, 1],
['Sm', 'Samarium', 150.36, 1],
['Eu', 'Europium', 151.964, 1],
['Gd', 'Gadolinium', 157.25, 1],
['Tb', 'Terbium', 158.9253, 1],
['Dy', 'Dysprosium', 162.5, 1],
['Ho', 'Holmium', 164.9303, 1],
['Er', 'Erbium', 167.259, 1],
['Tm', 'Thulium', 168.9342, 1],
['Yb', 'Ytterbium', 173.04, 1],
['Lu', 'Lutetium', 174.967, 1],
['Hf', 'Hafnium', 178.49, 1],
['Ta', 'Tantalum', 180.9479, 1],
['W', 'Tungsten', 183.84, 1],
['Re', 'Rhenium', 186.207, 1],
['Os', 'Osmium', 190.23, 1],
['Ir', 'Iridium', 192.217, 1],
['Pt', 'Platinum', 195.078, 1],
['Au', 'Gold', 196.9665, 1],
['Hg', 'Mercury', 200.59, 1],
['Tl', 'Thallium', 204.3833, 1],
['Pb', 'Lead', 207.2, 1],
['Bi', 'Bismuth', 208.9804, 1],
['Po', 'Polonium', 209.0, 1],
['At', 'Astatine', 210.0, 1],
['Rn', 'Radon', 222.0, 1],
['Fr', 'Francium', 223.0, 1],
['Ra', 'Radium', 226.0, 1],
['Ac', 'Actinium', 227.0, 1],
['Th', 'Thorium', 232.0381, 1],
['Pa', 'Protactinium', 231.0359, 1],
['U', 'Uranium', 238.0289, 1],
['Np', 'Neptunium', 237.0, 1],
['Pu', 'Plutonium', 244.0, 1],
['Am', 'Americium', 243.0, 1],
['Cm', 'Curium', 247.0, 1],
['Bk', 'Berkelium', 247.0, 1],
['Cf', 'Californium', 251.0, 1],
['Es', 'Einsteinium', 252.0, 1],
['Fm', 'Fermium', 257.0, 1],
['Md', 'Mendelevium', 258.0, 1],
['No', 'Nobelium', 259.0, 1],
['Lr', 'Lawrencium', 262.0, 1],
['Rf', 'Rutherfordium', 261.0, 1],
['Db', 'Dubnium', 262.0, 1],
['Sg', 'Seaborgium', 266.0, 1],
['Bh', 'Bohrium', 264.0, 1],
['Hs', 'Hassium', 277.0, 1],
['Mt', 'Meitnerium', 268.0, 1]]

pt_config_exact = [
['H', 'Hydrogen', 1.007825, 0.9999],
['He', 'Helium', 4.002603, 1.0],
['Li', 'Lithium', 7.016005, 0.9258],
['Be', 'Beryllium', 9.012183, 1.0],
['B', 'Boron', 11.009305, 0.802],
['C', 'Carbon', 12.0, 0.989],
['N', 'Nitrogen', 14.003074, 0.9963],
['O', 'Oxygen', 15.994915, 0.9976],
['F', 'Fluorine', 18.998403, 1.0],
['Ne', 'Neon', 19.992439, 0.906],
['Na', 'Sodium', 22.98977, 1.0],
['Mg', 'Magnesium', 23.985045, 0.789],
['Al', 'Aluminum', 26.981541, 1.0],
['Si', 'Silicon', 27.976928, 0.9223],
['P', 'Phosphorus', 30.973763, 1.0],
['S', 'Sulfur', 31.972072, 0.9502],
['Cl', 'Chlorine', 34.968853, 0.7577],
['Ar', 'Argon', 39.962383, 0.996],
['K', 'Potassium', 38.963708, 0.932],
['Ca', 'Calcium', 39.962591, 0.9695],
['Sc', 'Scandium', 44.955914, 1.0],
['Ti', 'Titanium', 47.947947, 0.738],
['V', 'Vanadium', 50.943963, 0.9975],
['Cr', 'Chromium', 51.94051, 0.8379],
['Mn', 'Manganese', 54.938046, 1.0],
['Fe', 'Iron', 55.934939, 0.9172],
['Co', 'Cobalt', 58.933198, 1.0],
['Ni', 'Nickel', 57.935347, 0.6827],
['Cu', 'Copper', 62.929599, 0.6917],
['Zn', 'Zinc', 63.929145, 0.486],
['Ga', 'Gallium', 68.925581, 0.601],
['Ge', 'Germanium', 73.921179, 0.365],
['As', 'Arsenic', 74.921596, 1.0],
['Se', 'Selenium', 79.916521, 0.496],
['Br', 'Bromine', 78.918336, 0.5069],
['Kr', 'Krypton', 83.911506, 0.57],
['Rb', 'Rubidium', 84.9118, 0.7217],
['Sr', 'Strontium', 87.905625, 0.8258],
['Y', 'Yttrium', 88.905856, 1.0],
['Zr', 'Zirconium', 89.904708, 0.5145],
['Nb', 'Niobium', 92.906378, 1.0],
['Mo', 'Molybdenum', 97.905405, 0.2413],
['Ru', 'Ruthenium', 101.90434, 0.316],
['Rh', 'Rhodium', 102.905503, 1.0],
['Pd', 'Palladium', 105.903475, 0.2733],
['Ag', 'Silver', 106.905095, 0.5184],
['Cd', 'Cadmium', 113.903361, 0.2873],
['In', 'Indium', 114.903875, 0.957],
['Sn', 'Tin', 119.902199, 0.324],
['Sb', 'Antimony', 120.903824, 0.573],
['Te', 'Tellurium', 129.906229, 0.338],
['I', 'Iodine', 126.904477, 1.0],
['Xe', 'Xenon', 131.904148, 0.269],
['Cs', 'Cesium', 132.905433, 1.0],
['Ba', 'Barium', 137.905236, 0.717],
['La', 'Lanthanum', 138.906355, 0.9991],
['Ce', 'Cerium', 139.905442, 0.8848],
['Pr', 'Praseodymium', 140.907657, 1.0],
['Nd', 'Neodymium', 141.907731, 0.2713],
['Sm', 'Samarium', 151.919741, 0.267],
['Eu', 'Europium', 152.921243, 0.522],
['Gd', 'Gadolinium', 157.924111, 0.2484],
['Tb', 'Terbium', 158.92535, 1.0],
['Dy', 'Dysprosium', 163.929183, 0.282],
['Ho', 'Holmium', 164.930332, 1.0],
['Er', 'Erbium', 165.930305, 0.336],
['Tm', 'Thulium', 168.934225, 1.0],
['Yb', 'Ytterbium', 173.938873, 0.318],
['Lu', 'Lutetium', 174.940785, 0.974],
['Hf', 'Hafnium', 179.946561, 0.352],
['Ta', 'Tantalum', 180.948014, 0.9999],
['W', 'Tungsten', 183.950953, 0.3067],
['Re', 'Rhenium', 186.955765, 0.626],
['Os', 'Osmium', 191.961487, 0.41],
['Ir', 'Iridium', 192.962942, 0.627],
['Pt', 'Platinum', 194.964785, 0.338],
['Au', 'Gold', 196.96656, 1.0],
['Hg', 'Mercury', 201.970632, 0.2965],
['Tl', 'Thallium', 204.97441, 0.7048],
['Pb', 'Lead', 207.976641, 0.524],
['Bi', 'Bismuth', 208.980388, 1.0],
['Th', 'Thorium', 232.038054, 1.0],
['U', 'Uranium', 238.050786, 0.9927]]

class PeriodicTable(object):
    def __init__(self, elements):
        self._elements = elements
            
    def mw(self, name):
    	if name in self._elements._short_names:
    		short_name = name
    	elif name in self._elements._long_names:
    		short_name = self._elements.get_short_name(name)
    	else:
    		sys.exit('Element not in Periodic Table')
    	x = self._elements.mw(short_name)
    	return x
    	
    def get_element(self, name):
    	if name in self._elements._short_names:
    		short_name = name
    	elif name in self._elements._long_names:
    		short_name = self._elements.get_short_name(name)
    	else:
    		sys.exit('Element not in Periodic Table')
    	x = self._elements.get_element(short_name)
    	return x
      
class Elements(object):
	def __init__(self, element_list):
		self._element_list = element_list
		self._short_names = [x.short_name for x in self._element_list]
		if len(set(self._short_names)) != len(self._short_names):
			sys.exit('Duplicate Short Names')
		self._long_names = [x.long_name for x in self._element_list]
		if len(set(self._long_names)) != len(self._long_names):
			sys.exit('Duplicate Long Names')
		
	def mw(self, short_name):
		mw, = [x.molecular_weight for x in self._element_list if x.short_name == short_name]
		return mw
		
	def get_short_name(self, long_name):
		n, = [x.short_name for x in self._element_list if x.long_name == long_name]
		return n
		
	def get_element(self, short_name):
		e, = [x for x in self._element_list if x.short_name == short_name]
		return e
		
	
		
Element = namedtuple('Element', ['short_name', 'long_name', 'molecular_weight', 'abundance'])

def elements_factory(config, parts_class=Elements, part_class=Element):
	return parts_class([create_element(x, part_class) for x in config])
	
def create_element(config, part_class):
	return part_class(short_name=config[0], long_name=config[1], molecular_weight=config[2], abundance=config[3])

class ChemicalFormula(object):
	def __init__(self, cf_string, pt=PeriodicTable(elements_factory(test_config))):
		self._cf_string = cf_string
		self._pt = pt
		self._cf_broken_string = self._break_string(self._cf_string)
		self._element_string = [(self._pt.get_element(x[0]), x[1]) for x in self._cf_broken_string]
		self._cf_units = cfunits_factory(self._element_string)
		
	def _break_string(self, string):
		return [(x[0],int(x[1])) if x[1] else (x[0],1) for x in re.findall('([A-Z][a-z]?)([0-9]*)',string)]
		
	def __str__(self):
		return self._cf_string
		
	def mw(self):
		return sum([x.element.molecular_weight * x.number for x in self._cf_units])
		
	def abundance(self):
		lst = [x.element.abundance ** x.number for x in self._cf_units]
		a = lst[0]
		for x in lst[1:]:
		    a *= x
		return round(a,6)
	
		
class CFUnits(object):
	def __init__(self, cfunit_list):
		self._cfunit_list = cfunit_list
		
	def __iter__(self):
		return iter(self._cfunit_list)
		
CFUnit = namedtuple('CFUnit', ['element', 'number'])

def cfunits_factory(config, parts_class=CFUnits, part_class=CFUnit):
	return parts_class([create_cfunit(x, part_class) for x in config])
	
def create_cfunit(config, part_class):
	return part_class(element=config[0], number=config[1])
