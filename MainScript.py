# © 2021, 2022 Greg Ritacco

"""
Pattern Scripts plugin for JMRI Operations Pro
OPS = Operations Pattern Scripts
© 2021, 2022 Greg Ritacco
No restrictions on use, but I would appreciate the reference.
"""

import jmri
import java.awt
import javax.swing
import time

import sys
from os import path as OS_PATH

SCRIPT_DIR = 'OperationsPatternScripts'
# SCRIPT_DIR = 'OperationsPatternScripts-2.0.0.b1'
# SCRIPT_DIR = 'OperationsPatternScripts-2.0.0.b2'

PLUGIN_ROOT = OS_PATH.join(jmri.util.FileUtil.getPreferencesPath(), SCRIPT_DIR)

sys.path.append(PLUGIN_ROOT)
from opsEntities import PSE

PSE.JMRI = jmri
PSE.JAVA_AWT = java.awt
PSE.JAVX_SWING = javax.swing
PSE.TIME = time
PSE.SYS = sys
PSE.PLUGIN_ROOT = PLUGIN_ROOT

from opsEntities import Listeners
from opsBundle import Bundle

SCRIPT_NAME = 'OperationsPatternScripts.MainScript'
SCRIPT_REV = 20221010

PSE.ENCODING = PSE.readConfigFile('CP')['SE']

Bundle.BUNDLE_DIR = OS_PATH.join(PSE.PLUGIN_ROOT, 'opsBundle')
# Bundle.validatePluginBundle()
# PSE.BUNDLE = Bundle.getBundleForLocale()
PSE.BUNDLE = {}


class Model:

    def __init__(self):

        self.psLog = PSE.LOGGING.getLogger('OPS.Main.Model')

        return

    def validatePatternConfig(self):
        """To be reworked when mergeConfigFiles() is implemented."""

        if not PSE.validateConfigFileVersion():
            PSE.mergeConfigFiles()
            self.psLog.info('Previous PatternConfig.json merged with new')
            PSE.writeNewConfigFile()
            self.psLog.warning('New PatternConfig.json file created for this profile')

        return

    def makePatternScriptsPanel(self, pluginPanel):

        for subroutine in self.makeSubroutineList():
            pluginPanel.add(PSE.JAVX_SWING.Box.createRigidArea(PSE.JAVA_AWT.Dimension(0,10)))
            pluginPanel.add(subroutine)
            pluginPanel.setName('OPS Plugin Panel')
        return pluginPanel

    def makeSubroutineList(self):
        """Add a subroutine if its ['CP']['I*'] = true."""

        subroutineList = []
        controlPanelConfig = PSE.readConfigFile('CP')
        for include in controlPanelConfig['IL']:
            if controlPanelConfig[include]:
                xModule = __import__(include, fromlist=['Controller'])
                startUp = xModule.Controller.StartUp()
                subroutineFrame = startUp.makeSubroutineFrame()
                subroutineList.append(subroutineFrame)
                self.psLog.info(include + ' subroutine added to control panel')

        return subroutineList

class View:

    def __init__(self, scrollPanel):

        self.psLog = PSE.LOGGING.getLogger('OPS.Main.View')

        self.cpSettings = PSE.readConfigFile('CP')

        self.controlPanel = scrollPanel
        self.psPluginMenuItems = []
        self.isKeyFile = Bundle.validateKeyFile()

        return

    def makePsButton(self):

        psButton = PSE.JAVX_SWING.JButton()
        psButton.setText(PSE.BUNDLE[u'Pattern Scripts'])
        psButton.setName('psButton')

        return psButton

    def makePluginPanel(self):
        """Dealers choice, jPanel or Box."""

        # pluginPanel = PSE.JAVX_SWING.JPanel()
        pluginPanel = PSE.JAVX_SWING.Box(PSE.JAVX_SWING.BoxLayout.PAGE_AXIS)

        return pluginPanel

    def makeScrollPanel(self, pluginPanel):

        scrollPanel = PSE.JAVX_SWING.JScrollPane(pluginPanel)
        scrollPanel.border = PSE.JAVX_SWING.BorderFactory.createLineBorder(PSE.JAVA_AWT.Color.GRAY)

        return scrollPanel

    def getPsPluginMenuItems(self):

        return self.psPluginMenuItems

    def makePatternScriptsWindow(self):

        self.psLog.debug('makePatternScriptsWindow')

        uniqueWindow = PSE.JMRI.util.JmriJFrame()

        # asMenuItem = self.makeMenuItem(self.setAsDropDownText())
        jpMenuItem = self.makeMenuItem(self.setJpDropDownText())
        tpMenuItem = self.makeMenuItem(self.setTpDropDownText())
        o2oMenuItem = self.makeMenuItem(self.setOoDropDownText())
        ptMenuItem = self.makeMenuItem(self.setPtDropDownText())
        if not self.isKeyFile:
            ptMenuItem.setEnabled(False)
        rsMenuItem = self.makeMenuItem(self.setRsDropDownText())
        helpMenuItem = self.makeMenuItem(self.setHmDropDownText())
        gitHubMenuItem = self.makeMenuItem(self.setGhDropDownText())
        opsFolderMenuItem = self.makeMenuItem(self.setOfDropDownText())
        logMenuItem = self.makeMenuItem(self.setLmDropDownText())
        editConfigMenuItem = self.makeMenuItem(self.setEcDropDownText())

        toolsMenu = PSE.JAVX_SWING.JMenu(PSE.BUNDLE[u'Tools'])
        toolsMenu.add(PSE.JMRI.jmrit.operations.setup.OptionAction())
        toolsMenu.add(PSE.JMRI.jmrit.operations.setup.PrintOptionAction())
        toolsMenu.add(PSE.JMRI.jmrit.operations.setup.BuildReportOptionAction())
        # toolsMenu.add(asMenuItem)
        toolsMenu.add(jpMenuItem)
        toolsMenu.add(tpMenuItem)
        toolsMenu.add(o2oMenuItem)
        # toolsMenu.add(gsMenuItem)
        toolsMenu.add(editConfigMenuItem)
        toolsMenu.add(ptMenuItem)
        toolsMenu.add(rsMenuItem)

        helpMenu = PSE.JAVX_SWING.JMenu(PSE.BUNDLE[u'Help'])
        helpMenu.add(helpMenuItem)
        helpMenu.add(gitHubMenuItem)
        helpMenu.add(opsFolderMenuItem)
        helpMenu.add(logMenuItem)

        psMenuBar = PSE.JAVX_SWING.JMenuBar()
        psMenuBar.add(toolsMenu)
        psMenuBar.add(PSE.JMRI.jmrit.operations.OperationsMenu())
        psMenuBar.add(PSE.JMRI.util.WindowMenu(uniqueWindow))
        psMenuBar.add(helpMenu)

        configPanel = PSE.readConfigFile('CP')
        uniqueWindow.setName('patternScriptsWindow')
        uniqueWindow.setTitle(PSE.BUNDLE[u'Pattern Scripts'])
        uniqueWindow.addWindowListener(Listeners.PatternScriptsWindow())
        uniqueWindow.setJMenuBar(psMenuBar)
        uniqueWindow.add(self.controlPanel)
        # uniqueWindow.pack()
        uniqueWindow.setSize(configPanel['PW'], configPanel['PH'])
        uniqueWindow.setLocation(configPanel['PX'], configPanel['PY'])
        uniqueWindow.setVisible(True)

        return

    def makeMenuItem(self, itemMethod):
        """Makes all the items for the custom drop down menus."""

        itemText, itemName = itemMethod

        menuItem = PSE.JAVX_SWING.JMenuItem(itemText)
        menuItem.setName(itemName)
        self.psPluginMenuItems.append(menuItem)

        return menuItem

    def setJpDropDownText(self):
        """itemMethod - Set the drop down text per the config file PatternTracksSubroutine Include flag ['CP']['IJ']"""

        patternConfig = PSE.readConfigFile('CP')
        if patternConfig['jPlusSubroutine']:
            menuText = PSE.BUNDLE[u'Disable j Plus subroutine']
        else:
            menuText = PSE.BUNDLE[u'Enable j Plus subroutine']

        return menuText, 'jpItemSelected'

    def setTpDropDownText(self):
        """itemMethod - Set the drop down text per the config file PatternTracksSubroutine Include flag ['CP']['IT']"""

        patternConfig = PSE.readConfigFile('CP')
        if patternConfig['PatternTracksSubroutine']:
            menuText = PSE.BUNDLE[u'Disable Track Pattern subroutine']
        else:
            menuText = PSE.BUNDLE[u'Enable Track Pattern subroutine']

        return menuText, 'tpItemSelected'

    def setOoDropDownText(self):
        """itemMethod - Set the drop down text per the config file o2oSubroutine Include flag ['CP']['IO']"""

        patternConfig = PSE.readConfigFile('CP')
        if patternConfig['o2oSubroutine']:
            menuText = PSE.BUNDLE[u'Disable o2o subroutine']
        else:
            menuText = PSE.BUNDLE[u'Enable o2o subroutine']

        return menuText, 'ooItemSelected'

    def setPtDropDownText(self):
        """itemMethod - Set the drop down text for the Translate Plugin item."""

        menuText = PSE.BUNDLE[u'Translate Plugin']

        return menuText, 'ptItemSelected'

    def setRsDropDownText(self):
        """itemMethod - Set the drop down text for the Restart From Default item."""

        menuText = PSE.BUNDLE[u'Restart From Default']

        return menuText, 'rsItemSelected'

    def setHmDropDownText(self):
        """itemMethod - Set the drop down text for the Log menu item."""

        menuText = PSE.BUNDLE[u'Window Help...']

        return menuText, 'helpItemSelected'

    def setLmDropDownText(self):
        """itemMethod - Set the drop down text for the Log menu item."""

        menuText = PSE.BUNDLE[u'View Log File']

        return menuText, 'logItemSelected'

    def setGhDropDownText(self):
        """itemMethod - Set the drop down text for the gitHub page item."""

        menuText = PSE.BUNDLE[u'GitHub Web Page']

        return menuText, 'ghItemSelected'

    def setEcDropDownText(self):
        """itemMethod - Set the drop down text for the edit config file item."""

        menuText = PSE.BUNDLE[u'Edit Config File']

        return menuText, 'ecItemSelected'

    def setOfDropDownText(self):
        """itemMethod - Set the drop down text for the operations folder item."""

        menuText = PSE.BUNDLE[u'Operations Folder']

        return menuText, 'ofItemSelected'

class Controller(PSE.JMRI.jmrit.automat.AbstractAutomaton):

    def init(self):
        """ """

        PSE.makeBuildStatusFolder()

        logFileTarget = PSE.OS_PATH.join(PSE.PROFILE_PATH, 'operations', 'buildstatus', 'PatternScriptsLog.txt')

        self.logger = PSE.Logger(logFileTarget)
        self.logger.startLogger('OPS')

        self.model = Model()

        self.trainsTableModel = PSE.JMRI.jmrit.operations.trains.TrainsTableModel()
        self.builtTrainListener = Listeners.BuiltTrain()
        self.trainsTableListener = Listeners.TrainsTable(self.builtTrainListener)

        self.menuItemList = []

        return

    def addPatternScriptsButton(self):
        """The Pattern Scripts button on the PanelPro frame."""

        self.patternScriptsButton = View(None).makePsButton()
        self.patternScriptsButton.actionPerformed = self.patternScriptsButtonAction
        PSE.APPS.buttonSpace().add(self.patternScriptsButton)
        PSE.APPS.buttonSpace().revalidate()

        return

    def addTrainsTableListener(self):

        self.trainsTableModel.addTableModelListener(self.trainsTableListener)

        return

    def removeTrainsTableListener(self):

        self.trainsTableModel.removeTableModelListener(self.trainsTableListener)

        return

    def addBuiltTrainListener(self):

        trainList = PSE.TM.getTrainsByIdList()
        for train in trainList:
            train.addPropertyChangeListener(self.builtTrainListener)

        return

    def removeBuiltTrainListener(self):

        trainList = PSE.TM.getTrainsByIdList()
        for train in trainList:
            train.removePropertyChangeListener(self.builtTrainListener)

        return

    def patternScriptsButtonAction(self, MOUSE_CLICKED):

        self.psLog.debug(MOUSE_CLICKED)

        self.buildThePlugin()

        return

    def closePsWindow(self):
        """Used by:
            tpItemSelected
            shutdownPlugin
            """

        for frame in PSE.JMRI.util.JmriJFrame.getFrameList():
            if frame.getName() == 'patternScriptsWindow':
                PSE.updateWindowParams(frame)
                PSE.closeSetCarsWindows()

                frame.setVisible(False)
                frame.dispose()

        return

    def buildThePlugin(self):
        """Used by:
            tpItemSelected
            startupPlugin
            patternScriptsButtonAction
            """

        view = View(None)
        emptyPluginPanel = view.makePluginPanel()
        populatedPluginPanel = self.model.makePatternScriptsPanel(emptyPluginPanel)

        scrollPanel = view.makeScrollPanel(populatedPluginPanel)
        patternScriptsWindow = View(scrollPanel)
        patternScriptsWindow.makePatternScriptsWindow()
        self.menuItemList = patternScriptsWindow.getPsPluginMenuItems()

        self.addMenuItemListeners()

        return

    def o2oSubroutineListeners(self):

        self.addTrainsTableListener()
        self.addBuiltTrainListener()

        return

    def addMenuItemListeners(self):
        """Use the pull down item names as the attribute to set the
            listener: asItemSelected, jpItemSelected, tpItemSelected, ooItemSelected, logItemSelected, helpItemSelected, Etc.
            Used by:
            buildThePlugin
            """

        for menuItem in self.menuItemList:
            menuItem.addActionListener(getattr(self, menuItem.getName()))

        return

    def jpItemSelected(self, JP_ACTIVATE_EVENT):
        """menu item-Tools/Enable j Plus Subroutine."""

        self.psLog.debug(JP_ACTIVATE_EVENT)
        patternConfig = PSE.readConfigFile()
        self.OSU = PSE.JMRI.jmrit.operations.setup


        if patternConfig['CP']['jPlusSubroutine']: # If enabled, turn it off
            patternConfig['CP']['jPlusSubroutine'] = False
            JP_ACTIVATE_EVENT.getSource().setText(PSE.BUNDLE[u'Enable j Plus subroutine'])

            self.OSU.Setup.setRailroadName(patternConfig['CP']['LN'])

            self.psLog.info('j Plus support deactivated')
            print('j Plus support deactivated')
        else:
            patternConfig['CP']['jPlusSubroutine'] = True
            JP_ACTIVATE_EVENT.getSource().setText(PSE.BUNDLE[u'Disable j Plus subroutine'])

            patternConfig['CP']['LN'] = self.OSU.Setup.getRailroadName()
            jPlusHeader = PSE.jPlusHeader().replace(';', '\n')
            self.OSU.Setup.setRailroadName(jPlusHeader)

            self.psLog.info('j Plus support activated')
            print('j Plus support activated')

        PSE.writeConfigFile(patternConfig)
        self.shutdownPlugin()
        self.startupPlugin()
        return

    def tpItemSelected(self, TP_ACTIVATE_EVENT):
        """menu item-Tools/Enable Track Pattern subroutine"""

        self.psLog.debug(TP_ACTIVATE_EVENT)
        patternConfig = PSE.readConfigFile()

        if patternConfig['CP']['PatternTracksSubroutine']: # If enabled, turn it off
            patternConfig['CP']['PatternTracksSubroutine'] = False
            TP_ACTIVATE_EVENT.getSource().setText(PSE.BUNDLE[u'Enable Track Pattern subroutine'])

            self.psLog.info('Track Pattern support deactivated')
            print('Track Pattern support deactivated')
        else:
            patternConfig['CP']['PatternTracksSubroutine'] = True
            TP_ACTIVATE_EVENT.getSource().setText(PSE.BUNDLE[u'Disable Track Pattern subroutine'])

            self.psLog.info('Track Pattern support activated')
            print('Track Pattern support activated')

        PSE.writeConfigFile(patternConfig)
        self.closePsWindow()
        self.buildThePlugin()

        return

    def ooItemSelected(self, O2O_ACTIVATE_EVENT):
        """menu item-Tools/Enable o2o subroutine"""

        self.psLog.debug(O2O_ACTIVATE_EVENT)
        patternConfig = PSE.readConfigFile()

        if patternConfig['CP']['o2oSubroutine']: # If enabled, turn it off
            patternConfig['CP']['o2oSubroutine'] = False
            O2O_ACTIVATE_EVENT.getSource().setText(PSE.BUNDLE[u'Enable o2o subroutine'])

            self.removeTrainsTableListener()
            self.removeBuiltTrainListener()

            self.psLog.info('o2o subroutine deactivated')
            print('o2o subroutine deactivated')
        else:
            patternConfig['CP']['o2oSubroutine'] = True
            O2O_ACTIVATE_EVENT.getSource().setText(PSE.BUNDLE[u'Disable o2o subroutine'])

            self.addTrainsTableListener()
            self.addBuiltTrainListener()

            self.psLog.info('o2o subroutine activated')
            print('o2o subroutine activated')

        PSE.writeConfigFile(patternConfig)
        self.shutdownPlugin()
        self.startupPlugin()

        return

    def ptItemSelected(self, TRANSLATE_PLUGIN_EVENT):
        """menu item-Tools/Translate Plugin"""

        self.psLog.debug(TRANSLATE_PLUGIN_EVENT)

        textBundles = Bundle.getAllTextBundles()
        Bundle.makePluginBundle(textBundles)

        Bundle.makeHelpBundle()
        Bundle.makeHelpPage()

        self.shutdownPlugin()
        self.startupPlugin()

        self.psLog.info('Pattern Scripts plugin translated')
        self.psLog.info('Pattern Scripts plugin restarted')

        return

    def rsItemSelected(self, RESTART_PLUGIN_EVENT):
        """menu item-Tools/Restart Plugin"""

        self.psLog.debug(RESTART_PLUGIN_EVENT)

        PSE.deleteConfigFile()

        self.shutdownPlugin()
        self.startupPlugin()

        self.psLog.info('Pattern Scripts plugin restarted')

        return

    def helpItemSelected(self, OPEN_HELP_EVENT):
        """menu item-Help/Window help..."""

        self.psLog.debug(OPEN_HELP_EVENT)

        stubFileTarget = PSE.OS_PATH.join(PSE.JMRI.util.FileUtil.getPreferencesPath(), 'jmrihelp', PSE.psLocale()[:2], 'psStub.html')
        stubUri = PSE.JAVA_IO.File(stubFileTarget).toURI()
        if PSE.JAVA_IO.File(stubUri).isFile():
            PSE.JAVA_AWT.Desktop.getDesktop().browse(stubUri)
        else:
            self.psLog.warning('Help file not found')

        return

    def logItemSelected(self, OPEN_LOG_EVENT):
        """menu item-Help/View Log"""

        self.psLog.debug(OPEN_LOG_EVENT)

        patternLog = PSE.makePatternLog()

        logFileTarget = PSE.OS_PATH.join(PSE.PROFILE_PATH, 'operations', 'buildstatus', 'PatternScriptsLog_temp.txt')

        PSE.genericWriteReport(logFileTarget, patternLog)
        PSE.genericDisplayReport(logFileTarget)

        print(SCRIPT_NAME + ' ' + str(SCRIPT_REV))

        return

    def ghItemSelected(self, OPEN_GH_EVENT):
        """menu item-Help/GitHub Page"""

        self.psLog.debug(OPEN_GH_EVENT)

        ghURL = 'https://github.com/gar-codespace/OperationsPatternScripts'
        PSE.JMRI.util.HelpUtil.openWebPage(ghURL)

        return

    def ecItemSelected(self, OPEN_EC_EVENT):
        """menu item-Help/Edit Config File"""

        self.psLog.debug(OPEN_EC_EVENT)

        configTarget = PSE.OS_PATH.join(PSE.PROFILE_PATH, 'operations', 'PatternConfig.json')

        if PSE.JAVA_IO.File(configTarget).isFile():
            PSE.genericDisplayReport(configTarget)
        else:
            self.psLog.warning('Not found: ' + configTarget)

        return

    def ofItemSelected(self, OPEN_OF_EVENT):
        """menu item-Help/Operations Folder"""

        self.psLog.debug(OPEN_OF_EVENT)

        opsFolderPath = PSE.OS_PATH.join(PSE.PROFILE_PATH, 'operations')

        opsFolder = PSE.JAVA_IO.File(opsFolderPath)
        if opsFolder.exists():
            PSE.JAVA_AWT.Desktop.getDesktop().open(opsFolder)
        else:
            self.psLog.warning('Not found: ' + opsFolderPath)

        return

    def shutdownPlugin(self):
        """Used by:
            ptItemSelected
            rsItemSelected
            ooItemSelected
            """

        self.closePsWindow()

        return

    def startupPlugin(self):
        """Used by:
            ptItemSelected
            rsItemSelected
            ooItemSelected
            """

        PSE.BUNDLE = Bundle.getBundleForLocale()
        PSE.CreateStubFile().make()
        Bundle.makeHelpPage()

        self.buildThePlugin()

        return

    def handle(self):

        startTime = PSE.TIME.time()
        self.psLog = PSE.LOGGING.getLogger('OPS.Main.Controller')
        self.logger.initialLogMessage(self.psLog)

        self.model.validatePatternConfig()

        Bundle.validatePluginBundle()
        PSE.BUNDLE = Bundle.getBundleForLocale()
        Bundle.validateHelpBundle()
        PSE.CreateStubFile().make()
        Bundle.makeHelpPage()

        PSE.closeOutputPanel()
        PSE.makeReportFolders()
        PSE.CreateStubFile().make()
        if PSE.readConfigFile()['CP']['o2oSubroutine']:
            self.o2oSubroutineListeners()
        if PSE.readConfigFile()['CP']['AP']:
            self.addPatternScriptsButton()

        PSE.openSystemConsole()

        self.psLog.info('Current Pattern Scripts directory: ' + PLUGIN_ROOT)
        runTime = PSE.TIME.time() - startTime
        self.psLog.info('Main script run time (sec): ' + str(round(runTime, 4)))
        print('Current Pattern Scripts directory: ' + PLUGIN_ROOT)
        print(SCRIPT_NAME + ' ' + str(SCRIPT_REV))

        return False

Controller().start()
