corp_name = "CS Energy"
site_name = "Kogan Creek"
site_tag_prefix = 'KCK'
site_units = ['Unit 1']
site_unit_prefix = {'Unit 1': 'U1'}
site_blocks = ['blr', 'turb', 'airgas']

cascade_heaters = [
    'turb.lph1',
    'turb.lph2',
    'turb.lph3',
    'turb.lph4',
    'turb.hph6',
    'turb.hph7',
    ]

cascade_heater_sub_components = []
for CH in cascade_heaters:
    cascade_heater_sub_components.append('%s.condenser' %CH)
    cascade_heater_sub_components.append('%s.desuperheater' %CH)
    cascade_heater_sub_components.append('%s.drainCooler' %CH)


boilder_elements = [
    'blr.furn',
    'blr.econ',
    'blr.prh',
    'blr.srh',
    'blr.psh',
    'blr.ssh',
    'blr.fsh',
    ]

fans = [
    'airgas.fdf.fdf_a',
    'airgas.fdf.fdf_b',
    'airgas.idf.idf_a',
    'airgas.idf.idf_b',
    'airgas.paf.paf_a',
    'airgas.paf.paf_b',
    ]

mills = [
    'airgas.pulv.ml_a',
    'airgas.pulv.ml_b',
    'airgas.pulv.ml_c',
    'airgas.pulv.ml_d',
    'airgas.pulv.ml_e',
    'airgas.pulv.ml_f',
    ]

turbine_stages = [
    'turb.hpc7',
    'turb.ipc6',
    'turb.ipc5',
    'turb.ipc4',
    'turb.lpc1_3',
    'turb.lpc2_3',
    ]

generators = ['turb.gen']

pumps = ['turb.cep', 'turb.bfp']

air_heaters = ['airgas.ah']


class ComponentClass(object):
     def __init__(self, instance_name):
        self.name = instance_name
        self.model_name = None
        self.measures = {}
    
     def generate_tag_info(self):
        tag_info = {}
        for m in sorted(self.measures.keys()):
            tag_info['%s.%s' %(self.name, m)] = self.measures[m]
        return tag_info

     def get_block_name(self):
        return self.name.split('.')[0]


class CascadeHeader(ComponentClass):
    def __init__(self, instance_name):
        self.name = instance_name
        self.model_name = 'CascadeHeater'
        self.measures = {
            'dca.use': ('degC', 'Heater DCA'),
            'c1.dT.use': ('degC', 'Heater C1 Temp delta (actual)'),
            'c1.dT.design': ('degC', 'Heater C1 Temp delta (design)'),
            'LMTD.use': ('degC', 'Heter LMTD'),
            'ttd.use': ('degC', 'Heater TTD'),
            'util.use': ('', 'Heater Utilisation'),
            }

class CascadeHeaderSubComponent(ComponentClass):
    def __init__(self, instance_name):
        self.name = instance_name
        self.model_name = 'CascadeHeaderSubComponent'
        self.measures = {
            'heatTransfer.use': ('kW', 'Element Heat transfer'),
            'LMTD.use': ('degC', 'Element LMTD'),
            'thermalConductance.use': ('kJ/K', 'Element Thermal Conductance'),
        }

class BoilerElement(ComponentClass):
    def __init__(self, instance_name):
        self.name = instance_name
        self.model_name = 'BoilerElement'
        self.measures = {
            'heatTransfer.use': ('kW', 'Element Heat Transfer'),
            'LMTD.use': ('degC', 'Element LMTD'),
            'thermalConductance.use': ('kJ/K', 'Element Thermal Conductance'),
        }

class Fan(ComponentClass):
    def __init__(self, instance_name):
        self.name = instance_name
        self.model_name = 'Fan'
        self.measures = {
            'efficiency.use': ('', 'Fan Efficiency (fraction)'),
            'c1in.volFlow.use': ('m3/s', 'Fan Volume Flow'),
            'efficiency.percentage': ('%','Fan Efficiency (percentage)'),
        }

class Mill(ComponentClass):
    def __init__(self, instance_name):
        self.name = instance_name
        self.model_name = 'Mill'
        self.measures = {
            'loadFuelFlowRatio.use': ('', 'Mill Load/Fuel Flow Ratio'),
            'airFuelFlowRatio.use': ('', 'Mill Air/Flow Flow Ratio'),
        }

class TurbineStage(ComponentClass):
    def __init__(self, instance_name):
        self.name = instance_name
        self.model_name = 'TurbineStage'
        self.measures = {
            'stageEfficiency.use': ('', 'Turbine Stage Eff. (fraction)'),
            'c1.dP.use': ('kPa', 'Turbine Stage DP'),
            'c1in.prop.entropy.use': ('kJ/K', 'Turbine Stage Entropy'),
            'c1out.prop.energy.isentropic': ('kJ/kg', 'Turbine Stage Isentropic Energy'),
            'stageEfficiency.percentage': ('%', 'Turbine Stage Eff. (percentage)'),
        }

class Generator(ComponentClass):
    def __init__(self, instance_name):
        self.name = instance_name
        self.model_name = 'Generator'
        self.measures = {
            'c3.dT.use': ('degC', 'Generator Cooling Temp delta'),
        }

class Pump(ComponentClass):
    def __init__(self, instance_name):
        self.name = instance_name
        self.model_name = 'Pump'
        self.measures = {
            'efficiency.use': ('%','Pump Efficiency (percentage)'),
            'fluidPower.use': ('kW', 'Pump Fluid Power'),
            'c1.dQ.use': ('kW', 'Pump supply Power'),
            'c1in.prop.density.use': ('kg/m3', 'Pump inlet density'),
            'c1out.prop.density.use': ('kg/m3', 'Pump outlet density'),
            'inlet.velocity.use': ('m/s', 'Pump inlet velocity'),
            'outlet.velocity.use': ('m/s', 'Pump outlet velocity'),
        }

class AirHeater(ComponentClass):
    def __init__(self, instance_name):
        self.name = instance_name
        self.model_name = 'AirHeater'
        self.measures = {
            'c2.dP.use': ('kPa','AH Gas DP'),
            'c2.dT.use': ('degC','AH Gas DT'),
            'gasEfficiency.use': ('%', 'AH Gas Efficiency'),
            'leakage.percentage': ('%', 'AH Leakage (percentage)'),
            'xratio.use': ('','AH X Ratio'),
            'c1PA.dP.use': ('kPa', 'AH PA DP'),
        }


site_components = {
    AirHeater: air_heaters,
    BoilerElement: boilder_elements,
    CascadeHeader: cascade_heaters,
    CascadeHeaderSubComponent: cascade_heater_sub_components,
    Fan: fans,
    Generator: generators,
    Mill: mills,
    Pump: pumps,
    TurbineStage: turbine_stages,
}