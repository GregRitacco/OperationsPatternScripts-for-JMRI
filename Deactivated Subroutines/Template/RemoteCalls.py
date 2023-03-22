# coding=utf-8
# © 2023 Greg Ritacco

"""
Calls other subs make to this one
Keep this as light as possible.
"""

from opsEntities import PSE

SCRIPT_NAME = PSE.SCRIPT_DIR + '.' + __name__
SCRIPT_REV = 20230201

_psLog = PSE.LOGGING.getLogger('OPS.XX.RemoteCalls')


def startupCalls():
    """
    Methods called when this subroutine is initialized by the Main Script.
    These calls are not turned off.
    """

    # configFile = PSE.readConfigFile()
    # if configFile['Main Script']['CP'][__package__]:

    return

def activatedCalls():
    """Methods called when this subroutine is activated."""

    # configFile = PSE.readConfigFile()
    # if configFile['Main Script']['CP'][__package__]:

    return

def deActivatedCalls():
    """Methods called when this subroutine is deactivated."""

    return

def refreshCalls():
    """Methods called when the subroutine needs to be refreshed."""

    PSE.restartSubroutineByName(__package__)
    
    return

def resetCalls():
    """Methods called to reset this subroutine."""

   # Model.resetConfigFileItems()
   
    return
    
def specificCalls():
    """Methods called to run specific tasks."""

    return
    