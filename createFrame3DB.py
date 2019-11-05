from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class CreateFrame3DB(AFXDataDialog):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, 'Create Frame',
            self.OK|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
            

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')
            
        TabBook_1 = FXTabBook(p=self, tgt=None, sel=0,
            opts=TABBOOK_NORMAL,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING)
        tabItem = FXTabItem(p=TabBook_1, text='\xbb\xec\xc4\xfd\xcd\xc1', ic=None, opts=TAB_TOP_NORMAL,
            x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_1 = FXVerticalFrame(p=TabBook_1,
            opts=FRAME_RAISED|FRAME_THICK|LAYOUT_FILL_X,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        HFrame_1 = FXHorizontalFrame(p=TabItem_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        VFrame_1 = FXVerticalFrame(p=HFrame_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        AFXTextField(p=VFrame_1, ncols=12, labelText='\xc4\xa3\xd0\xcd\xc3\xfb\xb3\xc6\xa3\xba', tgt=form.modelNameKw, sel=0)
        AFXTextField(p=VFrame_1, ncols=12, labelText='\xbf\xf2\xbc\xdc\xc3\xfb\xb3\xc6\xa3\xba', tgt=form.partNameKw, sel=0)
        VFrame_2 = FXVerticalFrame(p=HFrame_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        AFXTextField(p=VFrame_2, ncols=12, labelText='\xb2\xe3\xca\xfd\xa3\xba         ', tgt=form.nFloorKw, sel=0)
        AFXTextField(p=VFrame_2, ncols=12, labelText='\xba\xe1\xcf\xf2\xb7\xbf\xbc\xe4\xca\xfd\xa3\xba', tgt=form.nXKw, sel=0)
        AFXTextField(p=VFrame_2, ncols=12, labelText='\xd7\xdd\xcf\xf2\xb7\xbf\xbc\xe4\xca\xfd\xa3\xba', tgt=form.nZKw, sel=0)
        VFrame_3 = FXVerticalFrame(p=HFrame_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        FXRadioButton(p=VFrame_3, text='\xce\xde\xc2\xa5\xb0\xe5', tgt=form.slabSetKw1, sel=342)
        FXRadioButton(p=VFrame_3, text='\xb4\xf8\xc2\xa5\xb0\xe5', tgt=form.slabSetKw1, sel=343)
        AFXTextField(p=VFrame_3, ncols=12, labelText='\xc2\xa5\xb0\xe5\xba\xf1\xb6\xc8\xa3\xba', tgt=form.slab2Kw, sel=0)
        GroupBox_1 = FXGroupBox(p=TabItem_1, text='\xb9\xb9\xbc\xfe\xb3\xdf\xb4\xe7', opts=FRAME_GROOVE)
        HFrame_2 = FXHorizontalFrame(p=GroupBox_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        VFrame_4 = FXVerticalFrame(p=HFrame_2, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        GroupBox_2 = FXGroupBox(p=VFrame_4, text='\xd6\xf9', opts=FRAME_GROOVE)
        AFXTextField(p=GroupBox_2, ncols=12, labelText='\xb3\xa4\xa3\xba', tgt=form.column1Kw, sel=0)
        AFXTextField(p=GroupBox_2, ncols=12, labelText='\xbf\xed\xa3\xba', tgt=form.column3Kw, sel=0)
        AFXTextField(p=VFrame_4, ncols=12, labelText='\xb2\xe3\xb8\xdf\xa3\xba', tgt=form.column2Kw, sel=0)
        VFrame_5 = FXVerticalFrame(p=HFrame_2, opts=0, x=0, y=0, w=0, h=0,
            pl=25, pr=0, pt=0, pb=0)
        GroupBox_3 = FXGroupBox(p=VFrame_5, text='\xba\xe1\xc1\xba', opts=FRAME_GROOVE)
        AFXTextField(p=GroupBox_3, ncols=12, labelText='\xbf\xed\xa3\xba', tgt=form.beamx3Kw, sel=0)
        AFXTextField(p=GroupBox_3, ncols=12, labelText='\xb8\xdf\xa3\xba', tgt=form.beamx2Kw, sel=0)
        AFXTextField(p=VFrame_5, ncols=12, labelText='\xc1\xba\xbf\xe7\xa3\xba', tgt=form.beamx1Kw, sel=0)
        VFrame_6 = FXVerticalFrame(p=HFrame_2, opts=0, x=0, y=0, w=0, h=0,
            pl=25, pr=0, pt=0, pb=0)
        GroupBox_4 = FXGroupBox(p=VFrame_6, text='\xd7\xdd\xc1\xba', opts=FRAME_GROOVE)
        AFXTextField(p=GroupBox_4, ncols=12, labelText='\xbf\xed\xa3\xba', tgt=form.beamz1Kw, sel=0)
        AFXTextField(p=GroupBox_4, ncols=12, labelText='\xb8\xdf\xa3\xba', tgt=form.beamz2Kw, sel=0)
        AFXTextField(p=VFrame_6, ncols=12, labelText='\xc1\xba\xbf\xe7\xa3\xba', tgt=form.beamz3Kw, sel=0)
        tabItem = FXTabItem(p=TabBook_1, text='\xc5\xe4\xbd\xee', ic=None, opts=TAB_TOP_NORMAL,
            x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_2 = FXVerticalFrame(p=TabBook_1,
            opts=FRAME_RAISED|FRAME_THICK|LAYOUT_FILL_X,
            x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
            pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        GroupBox_5 = FXGroupBox(p=TabItem_2, text='\xd6\xf9\xc1\xba\xbd\xd8\xc3\xe6\xc5\xe4\xbd\xee\xca\xfd\xc1\xbf', opts=FRAME_GROOVE)
        HFrame_3 = FXHorizontalFrame(p=GroupBox_5, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        VFrame_7 = FXVerticalFrame(p=HFrame_3, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        GroupBox_6 = FXGroupBox(p=VFrame_7, text='\xd6\xf9', opts=FRAME_GROOVE)
        AFXTextField(p=GroupBox_6, ncols=12, labelText='x\xcf\xf2\xa3\xba', tgt=form.nc1Kw, sel=0)
        AFXTextField(p=GroupBox_6, ncols=12, labelText='z\xcf\xf2\xa3\xba', tgt=form.nc3Kw, sel=0)
        VFrame_8 = FXVerticalFrame(p=HFrame_3, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        GroupBox_7 = FXGroupBox(p=VFrame_8, text='\xba\xe1\xc1\xba', opts=FRAME_GROOVE)
        AFXTextField(p=GroupBox_7, ncols=12, labelText='\xc9\xcf\xb6\xcb\xa3\xba', tgt=form.nbxuKw, sel=0)
        AFXTextField(p=GroupBox_7, ncols=12, labelText='\xcf\xc2\xb6\xcb\xa3\xba', tgt=form.nbxdKw, sel=0)
        AFXTextField(p=GroupBox_7, ncols=12, labelText='y\xcf\xf2\xa3\xba  ', tgt=form.nbx2Kw, sel=0)
        VFrame_9 = FXVerticalFrame(p=HFrame_3, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        GroupBox_8 = FXGroupBox(p=VFrame_9, text='\xd7\xdd\xc1\xba', opts=FRAME_GROOVE)
        AFXTextField(p=GroupBox_8, ncols=12, labelText='\xc9\xcf\xb6\xcb\xa3\xba', tgt=form.nbzuKw, sel=0)
        AFXTextField(p=GroupBox_8, ncols=12, labelText='\xcf\xc2\xb6\xcb\xa3\xba', tgt=form.nbzdKw, sel=0)
        AFXTextField(p=GroupBox_8, ncols=12, labelText='y\xcf\xf2\xa3\xba  ', tgt=form.nbz2Kw, sel=0)
        GroupBox_9 = FXGroupBox(p=TabItem_2, text='\xc2\xa5\xb0\xe5\xc5\xe4\xbd\xee\xbc\xe4\xbe\xe0', opts=FRAME_GROOVE)
        HFrame_4 = FXHorizontalFrame(p=GroupBox_9, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        VFrame_10 = FXVerticalFrame(p=HFrame_4, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        AFXTextField(p=VFrame_10, ncols=12, labelText='x\xcf\xf2\xa3\xba', tgt=form.dsxKw, sel=0)
        VFrame_11 = FXVerticalFrame(p=HFrame_4, opts=0, x=0, y=0, w=0, h=0,
            pl=25, pr=0, pt=0, pb=0)
        AFXTextField(p=VFrame_11, ncols=12, labelText='z\xcf\xf2\xa3\xba', tgt=form.dszKw, sel=0)
