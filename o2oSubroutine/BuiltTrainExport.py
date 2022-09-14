"""Exports a JMRI manifest into a csv for import into the TrainPlayer o2o script suite.
    Callable from the pattern scripts subroutine or stand alone.
    """

import jmri
import time

SCRIPT_NAME ='OperationsPatternScripts.o2oSubroutine.BuiltTrainExport'
SCRIPT_REV = 20220101

SCRIPT_DIR = 'OperationsPatternScripts'
# SCRIPT_DIR = 'OperationsPatternScripts-2.0.0.b1'
# SCRIPT_DIR = 'OperationsPatternScripts-2.0.0.b2'

class StandAloneLogging():
    """Called when this script is used by itself"""

    def __init__(self):

        logPath = PatternScriptEntities.PROFILE_PATH  + 'operations\\buildstatus\\BuiltTrainExportLog.txt'
        self.logger = PatternScriptEntities.Logger(logPath)
        self.o2oLog = PatternScriptEntities.LOGGING.getLogger('TP.StandAlone')

        return

    def startLogging(self):

        self.logger.startLogger('TP')
        self.logger.initialLogMessage(self.o2oLog)

        return

    def stopLogging(self):

        self.logger.stopLogger('TP')

        return


class FindTrain:
    """Called when this script is used by itself"""

    def __init__(self):

        self.o2oLog = PatternScriptEntities.LOGGING.getLogger('TP.FindTrain')

        return

    def findNewestTrain(self):
        """If more than 1 train is built, pick the newest one"""

        self.o2oLog.debug('findNewestTrain')

        if not PatternScriptEntities.TM.isAnyTrainBuilt():

            return

        newestBuildTime = ''
        for train in self.getBuiltTrains():
            testDate = self.getTrainBuiltDate(train)
            if testDate > newestBuildTime:
                newestBuildTime = testDate
                newestTrain = train

        return newestTrain

    def getBuiltTrains(self):

        self.o2oLog.debug('getBuiltTrains')

        builtTrainList = []
        for train in PatternScriptEntities.TM.getTrainsByStatusList():
            if train.isBuilt():
                builtTrainList.append(train)

        return builtTrainList

    def getTrainBuiltDate(self, train):

        manifest = jmri.util.FileUtil.readFile(jmri.jmrit.operations.trains.JsonManifest(train).getFile())

        return PatternScriptEntities.loadJson(manifest)['date']


class ManifestForTrainPlayer(jmri.jmrit.automat.AbstractAutomaton):
    """Runs on JMRI train builds"""

    def init(self):

        self.SCRIPT_NAME = 'OperationsPatternScripts.o2oSubroutine.BuiltTrainExport.ManifestForTrainPlayer'
        self.SCRIPT_REV = 20220101

        self.standAloneLogging = StandAloneLogging()
        self.o2oLog = PatternScriptEntities.LOGGING.getLogger('TP.ManifestForTrainPlayer')

        return

    def getNewestTrain(self):

        return FindTrain().findNewestTrain()

    def passInTrain(self, train):

        self.train = train

        return

    def handle(self):

        self.standAloneLogging.startLogging()

        startTime = time.time()

        if not PatternScriptEntities.tpDirectoryExists():
            self.o2oLog.warning('TrainPlayer Reports directory not found')
            self.o2oLog.warning('TrainPlayer manifest export did not complete')

            return False

        self.o2oLog.debug('ModelWorkEvents.jmriManifestConversion')

        o2o = ModelWorkEvents.jmriManifestConversion(self.train)
        o2o.jmriManifestGetter()
        o2o.convertHeader()
        o2o.convertBody()
        o2oWorkEvents = o2o.geto2oWorkEvents()
    # Common post processor for ModelWorkEvents.ConvertPtMergedForm.o2oButton and BuiltTrainExport.ManifestForTrainPlayer.handle
        o2o = ModelWorkEvents.o2oWorkEvents(o2oWorkEvents)
        o2o.o2oHeader()
        o2o.o2oLocations()
        o2o.saveList()

        self.o2oLog.info('Export JMRI manifest to TrainPlyer: ' + self.train.getName())

        self.o2oLog.info('Export to TrainPlayer script location: ' + PLUGIN_ROOT)
        runTime = time.time() - startTime
        self.o2oLog.info('Manifest export (sec): ' + str(round(runTime, 4)))
        print(self.SCRIPT_NAME + ' ' + str(self.SCRIPT_REV))
        print('Manifest export (sec): ' + str(round(runTime, 4)))

        self.standAloneLogging.stopLogging()

        return False

if __name__ == "__builtin__":

    import jmri
    from sys import path as sysPath

    PLUGIN_ROOT = jmri.util.FileUtil.getPreferencesPath() + SCRIPT_DIR
    sysPath.append(PLUGIN_ROOT)
    from psEntities import PatternScriptEntities
    from o2oSubroutine import ModelWorkEvents
    from o2oSubroutine import ModelEntities
    from psBundle import Bundle

    Bundle.BUNDLE_DIR = PLUGIN_ROOT + '\\psBundle\\'

    PatternScriptEntities.PLUGIN_ROOT = PLUGIN_ROOT
    PatternScriptEntities.BUNDLE = Bundle.getBundleForLocale()
    PatternScriptEntities.ENCODING = 'utf-8'

    tpManifest = ManifestForTrainPlayer()
    newestTrain = tpManifest.getNewestTrain()
    if newestTrain:
        tpManifest.passInTrain(newestTrain)
        tpManifest.start()

else:

    PLUGIN_ROOT = jmri.util.FileUtil.getPreferencesPath() + SCRIPT_DIR
    from psEntities import PatternScriptEntities
    from o2oSubroutine import ModelWorkEvents
    from o2oSubroutine import ModelEntities
