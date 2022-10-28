# coding=utf-8
# © 2021, 2022 Greg Ritacco

"""The o2o Subroutine."""

from opsEntities import PSE
from o2oSubroutine import Model
from o2oSubroutine import ModelImport
from o2oSubroutine import View
from PatternTracksSubroutine import Controller as PtController

SCRIPT_NAME = 'OperationsPatternScripts.o2oSubroutine.Controller'
SCRIPT_REV = 20220101

_psLog = PSE.LOGGING.getLogger('OPS.o2o.Controller')


def updateO2oSubroutine(parent):
    """Allows other subroutines to update and restart the o2o Sub.
        Not implemented.
        """

    if not parent:
        return

    # Do stuff here.

    for component in parent.getComponents():
        if component.getName() == 'o2oSubroutine':
            restartSubroutine(component.getComponents()[0])

    return

def restartSubroutine(subroutineFrame):
    """Subroutine restarter.
        Used by:
        """

    subroutinePanel = StartUp(subroutineFrame).makeSubroutinePanel()
    subroutineFrame.removeAll()
    subroutineFrame.add(subroutinePanel)
    subroutineFrame.revalidate()

    return


class StartUp:
    """Start the o2o subroutine"""

    def __init__(self, subroutineFrame=None):

        self.subroutineFrame = subroutineFrame

        return

    def makeSubroutineFrame(self):
        """Makes the title border frame"""

        self.subroutineFrame = View.ManageGui().makeSubroutineFrame()
        subroutinePanel = self.makeSubroutinePanel()
        self.subroutineFrame.add(subroutinePanel)

        _psLog.info('o2o makeFrame completed')

        return self.subroutineFrame

    def makeSubroutinePanel(self):
        """Makes the control panel that sits inside the frame"""

        self.subroutinePanel, self.widgets = View.ManageGui().makeSubroutinePanel()
        self.activateWidgets()

        return self.subroutinePanel

    def activateWidgets(self):
        """The *.getName value is the name of the action for the widget.
            IE: newJmriRailroad, updateJmriRailroad
            """

        for widget in self.widgets:
            widget.actionPerformed = getattr(self, widget.getName())

        return

    def newJmriRailroad(self, EVENT):
        """Creates a new JMRI railroad from the tpRailroadData.json file"""

        _psLog.debug(EVENT)

        PSE.closeOutputPanel()

        if ModelImport.importTpRailroad():
            print('TrainPlayer railroad data imported OK')
            _psLog.info('TrainPlayer railroad data imported OK')
        else:
            print('TrainPlayer railroad not imported')
            _psLog.critical('TrainPlayer railroad not imported')
            return

        if Model.newJmriRailroad():
            parent = PSE.findPluginPanel(EVENT.getSource())
            PtController.updatePatternTracksSubroutine(parent)
            print('New JMRI railroad built from TrainPlayer data')
            _psLog.info('New JMRI railroad built from TrainPlayer data')
        else:
            print('New JMRI railroad not built')
            _psLog.critical('New JMRI railroad not built')

        print(SCRIPT_NAME + ' ' + str(SCRIPT_REV))

        return

    def updateJmriRailroad(self, EVENT):
        """Updates the locations data and writes new car and engine data."""

        _psLog.debug(EVENT)

        PSE.closeOutputPanel()

        if ModelImport.importTpRailroad():
            print('TrainPlayer railroad data imported OK')
            _psLog.info('TrainPlayer railroad data imported OK')
        else:
            print('TrainPlayer railroad not imported')
            _psLog.critical('TrainPlayer railroad not imported')
            return

        if Model.updateJmriRailroad():
            # parent = EVENT.getSource().getParent().getParent().getParent().getParent()
            parent = PSE.findPluginPanel(EVENT.getSource())
            PtController.updatePatternTracksSubroutine(parent)
            print('JMRI railroad updated from TrainPlayer data')
            _psLog.info('JMRI railroad updated from TrainPlayer data')
        else:
            print('JMRI railroad not updated')
            _psLog.critical('JMRI railroad not updated')

        print(SCRIPT_NAME + ' ' + str(SCRIPT_REV))

        return

    def updateJmriRollingingStock(self, EVENT):
        """Writes new car and engine data."""

        _psLog.debug(EVENT)

        PSE.closeOutputPanel()

        if ModelImport.importTpRailroad():
            print('TrainPlayer railroad data imported OK')
            _psLog.info('TrainPlayer railroad data imported OK')
        else:
            print('TrainPlayer railroad not imported')
            _psLog.critical('TrainPlayer railroad not imported')
            return

        if Model.updateJmriRollingingStock():
            print('JMRI rolling stock updated')
            _psLog.info('JMRI rolling stock updated')
        else:
            print('JMRI rolling stock not updated')
            _psLog.critical('JMRI rolling stock not updated')

        print(SCRIPT_NAME + ' ' + str(SCRIPT_REV))

        return
