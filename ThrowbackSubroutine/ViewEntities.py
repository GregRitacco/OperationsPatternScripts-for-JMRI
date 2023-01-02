# coding=utf-8
# © 2021, 2022 Greg Ritacco

"""
Template
"""

from opsEntities import PSE

SCRIPT_NAME = 'OperationsPatternScripts.ThrowbackSubroutine.ViewEntities'
SCRIPT_REV = 20221010

class tbSubroutinePanel:

    def __init__(self):
        """The *.setName value is the name of the action for the widget"""

        self.controlWidgets = []

        return

    def tbPanelMaker(self):

        tpPanel = PSE.JAVX_SWING.JPanel()

        ssButton = PSE.JAVX_SWING.JButton()
        ssButton.setText(PSE.BUNDLE[u'Snap Shot'])
        ssButton.setName('snapShot')
        self.controlWidgets.append(ssButton)

        pvButton = PSE.JAVX_SWING.JButton()
        pvButton.setText(PSE.BUNDLE[u'Previous'])
        pvButton.setName('previous')
        self.controlWidgets.append(pvButton)

        nxButton = PSE.JAVX_SWING.JButton()
        nxButton.setText(PSE.BUNDLE[u'Next'])
        nxButton.setName('next')
        self.controlWidgets.append(nxButton)

        tbButton = PSE.JAVX_SWING.JButton()
        tbButton.setText(PSE.BUNDLE[u'Throwback'])
        tbButton.setName('throwback')
        self.controlWidgets.append(tbButton)

        tpPanel.add(ssButton)
        tpPanel.add(PSE.JAVX_SWING.Box.createRigidArea(PSE.JAVA_AWT.Dimension(40,0)))
        tpPanel.add(pvButton)
        tpPanel.add(PSE.JAVX_SWING.Box.createRigidArea(PSE.JAVA_AWT.Dimension(20,0)))
        tpPanel.add(nxButton)
        tpPanel.add(PSE.JAVX_SWING.Box.createRigidArea(PSE.JAVA_AWT.Dimension(40,0)))
        tpPanel.add(tbButton)

        return tpPanel

    def tbWidgetGetter(self):

        return self.controlWidgets
