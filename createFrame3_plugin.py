#!/usr/bin/python
#-*-coding:UTF-8-*-
from abaqusGui import *
from abaqusConstants import ALL
import osutils, os


###########################################################################
# Class definition
###########################################################################

class CreateFrame3_plugin(AFXForm):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        
        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        self.radioButtonGroups = {}

        self.cmd = AFXGuiCommand(mode=self, method='createFrame',
            objectName='createFrame3', registerQuery=False)
        pickedDefault = ''
        self.modelNameKw = AFXStringKeyword(self.cmd, 'modelName', True, 'Model-1')
        self.partNameKw = AFXStringKeyword(self.cmd, 'partName', True, 'Frame')
        self.nFloorKw = AFXIntKeyword(self.cmd, 'nFloor', True)
        self.nXKw = AFXIntKeyword(self.cmd, 'nX', True)
        self.nZKw = AFXIntKeyword(self.cmd, 'nZ', True)
        if not self.radioButtonGroups.has_key('slabSet'):
            self.slabSetKw1 = AFXIntKeyword(None, 'slabSetDummy', True)
            self.slabSetKw2 = AFXStringKeyword(self.cmd, 'slabSet', True)
            self.radioButtonGroups['slabSet'] = (self.slabSetKw1, self.slabSetKw2, {})
        self.radioButtonGroups['slabSet'][2][342] = '\xce\xde\xc2\xa5\xb0\xe5'
        self.slabSetKw1.setValue(342)
        if not self.radioButtonGroups.has_key('slabSet'):
            self.slabSetKw1 = AFXIntKeyword(None, 'slabSetDummy', True)
            self.slabSetKw2 = AFXStringKeyword(self.cmd, 'slabSet', True)
            self.radioButtonGroups['slabSet'] = (self.slabSetKw1, self.slabSetKw2, {})
        self.radioButtonGroups['slabSet'][2][343] = '\xb4\xf8\xc2\xa5\xb0\xe5'
        self.slab2Kw = AFXFloatKeyword(self.cmd, 'slab2', True, 0.1)
        self.column1Kw = AFXFloatKeyword(self.cmd, 'column1', True, 0.3)
        self.column3Kw = AFXFloatKeyword(self.cmd, 'column3', True, 0.3)
        self.column2Kw = AFXFloatKeyword(self.cmd, 'column2', True, 3)
        self.beamx3Kw = AFXFloatKeyword(self.cmd, 'beamx3', True, 0.2)
        self.beamx2Kw = AFXFloatKeyword(self.cmd, 'beamx2', True, 0.4)
        self.beamx1Kw = AFXFloatKeyword(self.cmd, 'beamx1', True, 4)
        self.beamz1Kw = AFXFloatKeyword(self.cmd, 'beamz1', True, 0.2)
        self.beamz2Kw = AFXFloatKeyword(self.cmd, 'beamz2', True, 0.4)
        self.beamz3Kw = AFXFloatKeyword(self.cmd, 'beamz3', True, 4)
        self.nc1Kw = AFXIntKeyword(self.cmd, 'nc1', True, 2)
        self.nc3Kw = AFXIntKeyword(self.cmd, 'nc3', True, 2)
        self.nbxuKw = AFXIntKeyword(self.cmd, 'nbxu', True, 2)
        self.nbxdKw = AFXIntKeyword(self.cmd, 'nbxd', True, 2)
        self.nbx2Kw = AFXIntKeyword(self.cmd, 'nbx2', True, 2)
        self.nbzuKw = AFXIntKeyword(self.cmd, 'nbzu', True, 2)
        self.nbzdKw = AFXIntKeyword(self.cmd, 'nbzd', True, 2)
        self.nbz2Kw = AFXIntKeyword(self.cmd, 'nbz2', True, 2)
        self.dsxKw = AFXFloatKeyword(self.cmd, 'dsx', True, 0.15)
        self.dszKw = AFXFloatKeyword(self.cmd, 'dsz', True, 0.15)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):

        import createFrame3DB
        return createFrame3DB.CreateFrame3DB(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def doCustomChecks(self):

        # Try to set the appropriate radio button on. If the user did
        # not specify any buttons to be on, do nothing.
        #
        for kw1,kw2,d in self.radioButtonGroups.values():
            try:
                value = d[ kw1.getValue() ]
                kw2.setValue(value)
            except:
                pass
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def okToCancel(self):

        # No need to close the dialog when a file operation (such
        # as New or Open) or model change is executed.
        #
        return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Register the plug-in
#
thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerGuiMenuButton(
    buttonText='自定义|创建框架结构', 
    object=CreateFrame3_plugin(toolset),
    messageId=AFXMode.ID_ACTIVATE,
    icon=None,
    kernelInitString='import createFrame3',
    applicableModules=ALL,
    version='v3.0',
    author='Mahuijie',
    description='N/A',
    helpUrl='N/A'
)
