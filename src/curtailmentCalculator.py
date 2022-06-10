import datetime as dt
from typing import Dict
from src.contractInfoGenerator import CurtailmentCalculator
import os 

def calculateCurtailment(startDate:dt.datetime, endDate:dt.datetime, appConfig:Dict):

    noarFilesPath = appConfig['NoarFolderPath']
    wbesFilesPath = appConfig['WbesFolderPath']
    allWbesFiles  = os.listdir(wbesFilesPath)
    currDate = startDate

    while currDate<=endDate:
        dateStr1= dt.datetime.strftime(currDate, '%d%m%y')
        dateStr2= dt.datetime.strftime(currDate, '%d-%m-%Y')

        noarFilePath = noarFilesPath+ 'IMPSCH' + dateStr1 + '.csv'
        for wbesFile in allWbesFiles:
            if dateStr2 in wbesFile:
                wbesFilePath = wbesFilesPath + wbesFile
                
        obj_curtailmentCalculator = CurtailmentCalculator(noarFilePath, wbesFilePath)
        obj_curtailmentCalculator.doAll(dateStr2)
        currDate = currDate + dt.timedelta(days=1)