from typing import Dict
import pandas as pd



def addContractDetailsToDf(inputDf:pd.DataFrame, contractDetailsDict:Dict)->pd.DataFrame:
    """ add contract details to Idput dataframe

    Args:
        inputDf (pd.DataFrame): input dataframe of NOAR/WBES
        contractDetailsDict (Dict): all contract details dictionary with keys as contractId and value as list of details like
            [Type,
            Trader,
            Injecting State,
            Injecting Utility,
            Drawee State,
            Drawee Utility,
            Link,
            Path,
            ContractFromDate,
            ContractToDate
            ]

    Returns:
        pd.DataFrame: input dataframe of NOAR/WBES with contract details added in beginning
    """    
    inputDfCols= inputDf.columns.to_list()[2:]
    subdict = {x: contractDetailsDict[x] for x in inputDfCols if x in contractDetailsDict.keys()}
    contractDetailsDf = pd.DataFrame.from_dict(subdict)
    combineDf = pd.concat([contractDetailsDf, inputDf], axis=0)
    dateCol = combineDf.pop('DATE')
    blkCol = combineDf.pop('BLK')
    combineDf.insert(0, 'DATE', dateCol)
    combineDf.insert(1, 'BLK', blkCol)
    combineDf.reset_index(drop=True, inplace= True)
    return combineDf
    
def calculateDifference(noarDf:pd.DataFrame, wbesDf:pd.DataFrame)->pd.DataFrame:
    """ calculate curtailment dataframe

    Args:
        noarDf (pd.DataFrame): Input NOAR Dataframe
        wbesDf (pd.DataFrame): Input WBES Dataframe

    Returns:
        pd.DataFrame: Return Curtailment Dataframe
    """    

    curtailmentDf = pd.DataFrame()
    curtailmentDf['DATE'] = noarDf['DATE']
    curtailmentDf['BLK'] = noarDf['BLK']
    noarDf.sort_values(by=3, ascending=True, axis=1, inplace=True,  na_position= 'first')
    wbesDf.sort_values(by=3, ascending=True, axis=1, inplace=True, na_position= 'first' )

    noarCols= noarDf.columns.tolist()[2:]
    wbesCols = wbesDf.columns.tolist()[2:]

    for col in noarCols :
        if col in wbesCols:
            curtailmentDf.loc[:10,col] = noarDf.loc[:10,col]
            curtailmentDf.loc[10:,col] = noarDf.loc[10:,col]- wbesDf.loc[10:,col]
    
    
    return curtailmentDf
   
def filterCurtailmentDf(cutailmentDf:pd.DataFrame)->pd.DataFrame:
    """ Filter curtailment Dataframe with columns which have any value >0 or <0

    Args:
        cutailmentDf (pd.DataFrame): Curtailment Dataframe

    Returns:
        pd.DataFrame: Returns Filtered Curtailment Dataframe
    """    

    filteredCols = ['DATE', 'BLK']
    for col in cutailmentDf.columns.to_list()[2:]:
        for ind in cutailmentDf.index.tolist()[10:]:
            if (cutailmentDf[col][ind]>0) or  (cutailmentDf[col][ind]<0):
                filteredCols.append(col)
                break
    filteredCurtailmentDf = cutailmentDf[filteredCols]
    return filteredCurtailmentDf


    