from typing import Dict
import pandas as pd 

class FilteredNoarCalculator():
    """ class to calculate filtered NOAR dataframe
    """

    def __init__(self, noarfilePath:str):
        """ constructor method 

        Args:
            noarfilePath (str): NOAR file path for initialization of NOAR Dataframe.
        """        
        self.noarDf = pd.read_csv(noarfilePath)
        self.filteredNoarDf= None
        self.validContractIds= []

    def generateFilteredNoarDf(self, dateKey:str)->Dict:
        """ method to generate NOAR filtered Dataframe

        Args:
            dateKey (str): dtae key of current NOAR file

        Returns:
            Dict: {'filteredNoarDf': Filtered NOAR DF, 'contractDetailsDict': all contract details dictionary with keys as contractId and value as list of details}
        """        
       
        contractIdList = self.noarDf.columns.tolist()[1:]
        
        for contractId in contractIdList:
            pathStr = self.noarDf[contractId][7]
            pathList = pathStr.split('-')
            if len(pathList)==2 and pathList[1]== 'WR':
                self.validContractIds.append(contractId)
                continue
            if len(pathList)==3 and pathList[2]== 'WR':
                self.validContractIds.append(contractId)

              
        self.filteredNoarDf = self.noarDf[self.validContractIds].iloc[11:].reset_index(drop=True)
        cols = self.filteredNoarDf.columns.tolist()
        for col in cols :
            self.filteredNoarDf[col] = self.filteredNoarDf[col].astype('float')

        self.filteredNoarDf.insert(0, "DATE", dateKey)   
        self.filteredNoarDf.insert(1, "BLK", list(range(1, 97)) )
        # self.filteredNoarDf= self.filteredNoarDf.fillna(0)
        contractDetailsDict = self.generateContractDetails()
        return {'filteredNoarDf':self.filteredNoarDf, 'contractDetailsDict':contractDetailsDict}

    def generateContractDetails(self)->Dict:
        """return all contract details dictionary with keys as contractId and value as list of details

        Returns:
            Dict: all contract details dictionary with keys as contractId and value as list of details like
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
        """        
        contractDetailsDict = {}
        contractDetailsDf = self.noarDf[self.validContractIds].iloc[0:10]
        for col in contractDetailsDf.columns.to_list():
            contractDetailsDict[col]= contractDetailsDf[col].tolist()
        return contractDetailsDict

    