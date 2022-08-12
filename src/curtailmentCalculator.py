import datetime as dt
from typing import Dict
import pandas as pd
from src.filteredNoarGenerator import FilteredNoarCalculator
from src.filteredWbesGeneration import FilteredWbesCalculator
from src.helperFunctions import addContractDetailsToDf, calculateDifference, filterCurtailmentDf
import os 


def calculateCurtailment(startDate:dt.datetime, endDate:dt.datetime, appConfig:Dict)->None:
    """ calculate curtaillment and generate excel of NOAR, WBES and Curtailment details of STOA transactions.

    Args:
        startDate (dt.datetime): User StartDate
        endDate (dt.datetime): User EndDate
        appConfig (Dict): application configuration
    """    

    noarFilesPath = appConfig['NoarFolderPath']
    wbesFilesPath = appConfig['WbesDerivedFolderPath']
    reportDumpPath = appConfig['ReportDumpPath']
    isNoarFileReadingSuccess = True
    reportDumpFileName = f'{reportDumpPath}StoaCurtailment_{startDate.date()}To{endDate.date()}.xlsx' 
    allWbesFiles  = os.listdir(wbesFilesPath)
    currDate = startDate

    combineNoarDf = pd.DataFrame()
    combineWbesDf = pd.DataFrame()
    allContractDetailsDict ={}
    
    while currDate<=endDate:

        dateStr1= dt.datetime.strftime(currDate, '%d%m%y')
        dateStr2= dt.datetime.strftime(currDate, '%d-%m-%Y')
        noarFilePath = noarFilesPath+ 'IMPSCH' + dateStr1 + '.csv'
        try:
            obj_filteredNoarCalculator = FilteredNoarCalculator(noarFilePath)
        except Exception as err:
            print(f'{err}//// Please place NOAR file of {dateStr2} in desired folder.')
            isNoarFileReadingSuccess =False
            break
        filteredNoarDictData = obj_filteredNoarCalculator.generateFilteredNoarDf(dateStr2)
        combineNoarDf = pd.concat([combineNoarDf, filteredNoarDictData['filteredNoarDf']], axis=0)
        allContractDetailsDict = {**allContractDetailsDict, **filteredNoarDictData['contractDetailsDict']}
        currDate = currDate + dt.timedelta(days=1)
    
    validContIdMonth = list(allContractDetailsDict.keys())
    startDateStr= dt.datetime.strftime(startDate, '%d%m%y')
    endDateStr= dt.datetime.strftime(endDate, '%d%m%y')
    wbesFilePath=''
    for wbesFile in allWbesFiles:
            if (startDateStr in wbesFile) or (endDateStr in wbesFile):
                wbesFilePath = wbesFilesPath + wbesFile
    # read wbes file only if wbesfilePath is not null and noarfile reading is successfull
    if wbesFilePath!='' and isNoarFileReadingSuccess:
        obj_filteredWbesCalculator = FilteredWbesCalculator(wbesFilePath)
        combineWbesDf = obj_filteredWbesCalculator.generateFilteredWbesDf(startDate, endDate, validContIdMonth)
    
        wbesDfwithContDetails = addContractDetailsToDf(combineWbesDf, allContractDetailsDict)
        noarDfwithContDetails = addContractDetailsToDf(combineNoarDf, allContractDetailsDict)

        curtailmentDf = calculateDifference(noarDfwithContDetails,wbesDfwithContDetails )
        filteredCurtailmentDf = filterCurtailmentDf(curtailmentDf)

        print("---------- Excel Generation Started-----------------")
        with pd.ExcelWriter(reportDumpFileName) as writer:
    
            # use to_excel function and specify the sheet_name and index
            # to store the dataframe in specified sheet
            noarDfwithContDetails.to_excel(writer, sheet_name='NOAR', index=False)
            wbesDfwithContDetails.to_excel(writer, sheet_name='WBES', index=False)
            curtailmentDf.to_excel(writer, sheet_name='CURTAILMENT', index=False)
            filteredCurtailmentDf.to_excel(writer, sheet_name='FILTERED_CURTAILMENT', index=False)
        print("---------- Excel Generation Completed-----------------")
    else:
         print(f'Please place WBES file of {startDate.month}th month in desired folder.')
    
    