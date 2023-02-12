# coding=utf-8
# © 2023 Greg Ritacco

"""
Patterns
"""

from opsEntities import PSE
from Subroutines.Patterns import ModelEntities

SCRIPT_NAME = PSE.SCRIPT_DIR + '.' + __name__
SCRIPT_REV = 20230201

_psLog = PSE.LOGGING.getLogger('OPS.PT.Model')


def resetConfigFileItems():
    """Called from PSE.remoteCalls('resetCalls')"""

    configFile = PSE.readConfigFile()
    configFile['Patterns'].update({'PD':''})
    configFile['Patterns'].update({'PL':''})
    configFile['Patterns'].update({'PT':{}})
    configFile['Patterns'].update({'PA':False})

    PSE.writeConfigFile(configFile)

    return

def initializeLocations():
    """Initializes the Patterns section of the configFile.
        If entries are missing, makes new PT entries using initial values.
        Called by:
        Controller.StartUp.makeSubroutinePanel
        """

    _psLog.debug('updateLocations')

    configFile = PSE.readConfigFile()
    locations = []
# Setup divisions
    allDivisions = PSE.getAllDivisionNames()
    configFile['Patterns'].update({'AD': allDivisions})

    if len(allDivisions) != 0 and not configFile['Patterns']['PD']: # when this sub is initialized
        configFile['Patterns'].update({'PD': allDivisions[0]})

        _psLog.info('Set initial division in config file')
# Setup locations
    if not configFile['Patterns']['PL']: # when this sub is initialised

        division = configFile['Patterns']['PD']
        locations = PSE.getLocationNamesByDivision(division)
        if not locations:
            locations = PSE.getAllLocationNames()

        try:
            configFile['Patterns'].update({'PL': locations[0]})
            configFile['Patterns'].update({'AL': locations})
        except:
            _psLog.warning('Initial location and tracks not set in config file')

        _psLog.info('Set initial location and tracks in config file')

    PSE.writeConfigFile(configFile)

    return

def updateConfigFile(controls):
    """Updates the Patterns part of the config file
        Called by:
        Controller.StartUp.trackPatternButton
        Controller.StartUp.setCarsButton
        """

    _psLog.debug('updateConfigFile')

    configFile = PSE.readConfigFile()
    configFile['Patterns'].update({"PL": controls[1].getSelectedItem()})
    configFile['Patterns'].update({"PA": controls[2].selected})
    configFile['Patterns'].update({"PT": ModelEntities.updateTrackCheckBoxes(controls[3])})

    PSE.writeConfigFile(configFile)

    return controls

def validSelection():
    """Catches on the fly user edit of JMRI location and tracknames.
        patternTracks and allTracksAtLoc should be the same.
        Called by:
        Controller.StartUp.trackPatternButton
        Controller.StartUp.setCarsButton
        """

    _psLog.debug('validSelection')
    configFile = PSE.readConfigFile()
    patternLocation = configFile['Patterns']['PL']

    if not PSE.LM.getLocationByName(patternLocation): # test if user renames a location
        return False

    allTracksAtLoc = ModelEntities.getTrackNamesByLocation(None)
    patternTracks = configFile['Patterns']['PT']
    if list(set(allTracksAtLoc).difference(set(patternTracks))): # Test if track names were edited.
        return False

    return True

def getSelectedTracks():
    """Gets the track objects checked in the Track Pattern Subroutine."""

    patternTracks = PSE.readConfigFile('Patterns')['PT']

    return [track for track, include in sorted(patternTracks.items()) if include]

def newWorkList():
    """The work list is all the switchlists combined.
        Reset when the Set Cars button is pressed.
        """

    workList = initializeReportHeader()

    fileName = PSE.BUNDLE['ops-work-list'] + '.json'
    targetPath = PSE.OS_PATH.join(PSE.PROFILE_PATH, 'operations', 'jsonManifests', fileName)
    workList = PSE.dumpJson(workList)
    PSE.genericWriteReport(targetPath, workList)

    return

def initializeReportHeader():

    OSU = PSE.JMRI.jmrit.operations.setup
    configFile = PSE.readConfigFile()

    listHeader = {}
    listHeader['railroadName'] = unicode(OSU.Setup.getRailroadName(), PSE.ENCODING)

    listHeader['railroadDescription'] = configFile['Patterns']['RD']
    listHeader['trainName'] = configFile['Patterns']['TN']
    listHeader['trainDescription'] = configFile['Patterns']['TD']
    listHeader['trainComment'] = configFile['Patterns']['TC']
    listHeader['division'] = configFile['Patterns']['PD']
    listHeader['date'] = unicode(PSE.validTime(), PSE.ENCODING)
    listHeader['locations'] = [{'locationName': configFile['Patterns']['PL'], 'tracks': [{'cars': [], 'locos': [], 'length': '', 'trackname': ''}]}]

    return listHeader

def makeTrackPattern(trackList=None):
    """Called by:
        Model.trackPatternButton
        View.setRsButton
        """

    if not trackList:
        trackList = getSelectedTracks()

    detailsForTrack = []
    patternLocation = PSE.readConfigFile('Patterns')['PL']
    for trackName in trackList:
        detailsForTrack.append(ModelEntities.getGenericTrackDetails(patternLocation, trackName))

    trackPattern = {}
    trackPattern['locationName'] = patternLocation
    trackPattern['tracks'] = detailsForTrack

    return trackPattern
























def appendWorkList(mergedForm):

    tracks = mergedForm['locations'][0]['tracks'][0]

    fileName = PSE.BUNDLE['ops-work-list'] + '.json'
    targetPath = PSE.OS_PATH.join(PSE.PROFILE_PATH, 'operations', 'jsonManifests', fileName)
    currentWorkList = PSE.jsonLoadS(PSE.genericReadReport(targetPath))

    currentWorkList['locations'][0]['tracks'].append(tracks)
    currentWorkList = PSE.dumpJson(currentWorkList)

    PSE.genericWriteReport(targetPath, currentWorkList)

    return

def patternReport():
    """Mini controller when the Track Pattern Report button is pressed
        Creates the Track Pattern data
        Called by:
        Controller.StartUp.patternReportButton
        """

    fileName = PSE.BUNDLE['ops-pattern-report'] + '.json'
    targetPath = PSE.OS_PATH.join(PSE.PROFILE_PATH, 'operations', 'jsonManifests', fileName)

    trackPattern = makeTrackPattern()
    trackPatternReport = makeTrackPatternReport(trackPattern)
    trackPatternReport = PSE.dumpJson(trackPatternReport)
    PSE.genericWriteReport(targetPath, trackPatternReport)

    return





def makeTrackPatternReport(trackPattern):
    """Called by:
        Model.trackPatternButton
        View.setRsButton
        """

    trackPatternReport = initializeReportHeader()
    parseName = trackPatternReport['railroadName'].replace(';', '\n')
    trackPatternReport.update({'railroadName':parseName})

    division = PSE.getDivisionForLocation(trackPatternReport['locations'][0]['locationName'])
    trackPatternReport.update({'division':division})

# put in as a list to maintain compatability with JSON File Format/JMRI manifest export.
    trackPatternReport['locations'] = [trackPattern]

    return trackPatternReport





def jDivision(selectedItem):
    """Updates the Division: combo box and ripples the changes.
        jDivisions is also the name of the combobox.
        """

    _psLog.debug('jDivision')

    configFile = PSE.readConfigFile()
    newDivision = ModelEntities.testSelectedDivision(selectedItem)
    newDivisionList = PSE.getAllDivisionNames()
    newLocationList = PSE.getLocationNamesByDivision(selectedItem)
    if len(newLocationList) == 0:
        newLocationList = PSE.getAllLocationNames()

    configFile['Patterns'].update({'PD': newDivision})
    configFile['Patterns'].update({'AD': newDivisionList})
    configFile['Patterns'].update({'PL': newLocationList[0]})
    configFile['Patterns'].update({'AL': newLocationList})

    PSE.writeConfigFile(configFile)
    PSE.restartSubroutineByName(__package__)

    # _psLog.info('The track list for division ' + str(selectedItem) + ' has been created')
    return

def jLocations(selectedItem):
    """Updates the Locations: combobox and ripples the changes.
        jLocations is also the name of the combobox.
        """

    _psLog.debug('jLocations')

    configFile = PSE.readConfigFile()
    newLocation = ModelEntities.testSelectedLocation(selectedItem)
    newLocationList = PSE.getAllLocationNames()

    configFile['Patterns'].update({'PL': newLocation})
    configFile['Patterns'].update({'AL': newLocationList})

    PSE.writeConfigFile(configFile)
    PSE.restartSubroutineByName(__package__)

    return




