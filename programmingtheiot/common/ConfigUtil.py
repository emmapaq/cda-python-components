"""
Configuration Utility Module for CDA.

A simple wrapper around Python's configparser, implemented
as a Singleton. Supports loading configuration files and
credential files for sections.
"""

import configparser
import logging
import os
import traceback
from pathlib import Path

from programmingtheiot.common.Singleton import Singleton
from programmingtheiot.common.ConfigConst import (
    DEFAULT_CONFIG_FILE_NAME,
    CRED_SECTION,
    CRED_FILE_KEY,
    PARENT_PATH
)

class ConfigUtil(metaclass=Singleton):
    """
    ConfigUtil: Singleton wrapper for configparser.
    """

    configFile: str = DEFAULT_CONFIG_FILE_NAME
    configParser: configparser.ConfigParser = configparser.ConfigParser()
    isLoaded: bool = False

    def __init__(self, configFile: str = None):
        if configFile:
            self.configFile = configFile
        self._loadConfig()
        logging.info(f"Created instance of ConfigUtil: {self}")

    #
    # Public methods
    #

    def getConfigFileName(self) -> str:
        return self.configFile

    def getCredentials(self, section: str) -> dict:
        if self.hasSection(section):
            credFileName = self.getProperty(section, CRED_FILE_KEY)
            try:
                if os.path.isfile(credFileName):
                    logging.info(f"Loading credentials from section {section} and file {credFileName}")
                    # Read cred data and wrap in a section
                    fileRef = Path(credFileName)
                    credData = f"[{CRED_SECTION}]\n{fileRef.read_text()}"

                    credParser = configparser.ConfigParser()
                    credParser.optionxform = str  # preserve case
                    credParser.read_string(credData)
                    return dict(credParser.items(CRED_SECTION))
                else:
                    logging.warning(f"Credential file doesn't exist: {credFileName}")
            except Exception as e:
                logging.error(f"Failed to load credentials from file: {credFileName}. Exception: {e}")
                traceback.print_exc()
        return None

    def getProperty(self, section: str, key: str, defaultVal: str = None, forceReload: bool = False):
        return self._getConfig(forceReload).get(section, key, fallback=defaultVal)

    def getBoolean(self, section: str, key: str, forceReload: bool = False) -> bool:
        return self._getConfig(forceReload).getboolean(section, key, fallback=False)

    def getInteger(self, section: str, key: str, defaultVal: int = 0, forceReload: bool = False) -> int:
        return self._getConfig(forceReload).getint(section, key, fallback=defaultVal)

    def getFloat(self, section: str, key: str, defaultVal: float = 0.0, forceReload: bool = False) -> float:
        return self._getConfig(forceReload).getfloat(section, key, fallback=defaultVal)

    def hasProperty(self, section: str, key: str) -> bool:
        return self._getConfig().has_option(section, key)

    def hasSection(self, section: str) -> bool:
        return self._getConfig().has_section(section)

    def isConfigDataLoaded(self) -> bool:
        return self.isLoaded

    #
    # Private methods
    #

    def _loadConfig(self):
        # 1) User-provided file
        if self.configFile != DEFAULT_CONFIG_FILE_NAME:
            logging.info(f"Loading user config: {self.configFile}")
            self._doLoadConfig(configFilePath=self.configFile)

        # 2) Default config file
        if not self.isLoaded:
            logging.info(f"Loading default config: {self.configFile}")
            self._doLoadConfig(configFilePath=self.configFile)

        # 3) Relative parent path
        if not self.isLoaded:
            self.configFile = os.path.join(PARENT_PATH, self.configFile)
            logging.info(f"Loading config from parent path: {self.configFile}")
            self._doLoadConfig(configFilePath=self.configFile)

        if not self.isLoaded:
            logging.warning("No config file loaded. System running without proper configuration.")
        else:
            logging.debug(f"Config sections loaded: {self.configParser.sections()}")

    def _doLoadConfig(self, configFilePath: str):
        if os.path.exists(configFilePath):
            logging.info(f"Path found. Loading config file: {configFilePath}")
            self.configParser.read(configFilePath)
            self.isLoaded = True
            logging.info(f"Config file successfully loaded from: {configFilePath}")
        else:
            logging.warning(f"Path not found. Failed to load config file: {configFilePath}")

    def _getConfig(self, forceReload: bool = False) -> configparser.ConfigParser:
        if not self.isLoaded or forceReload:
            self._loadConfig()
        return self.configParser
