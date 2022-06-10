import pandas as pd 

class CurtailmentCalculator():
    noarDf:pd.DataFrame = None
    filteredNoarDf:pd.DataFrame = None
    filteredWbesDf:pd.DataFrame = None

    def __init__(self, noarfilePath:str, wbesFilePath:str ):
        self.noarDf = pd.read_csv(noarfilePath)
        self.wbesDf = pd.read_csv(wbesFilePath, skiprows=6)
        print(self.wbesDf)

    def generateFilteredNoarWbesDf(self, dateKey:str):
       
        contractIdList = self.noarDf.columns.tolist()[1:]
        validContractIds = []

        for contractId in contractIdList:
            pathStr = self.noarDf[contractId][7]
            pathList = pathStr.split('-')
            if len(pathList)==2:
                validContractIds.append(contractId)
                continue
            if len(pathList)==3 and pathList[1]!= 'WR':
                validContractIds.append(contractId)
        self.filteredNoarDf = self.noarDf[validContractIds].iloc[11:]
        # self.filteredWbesDf = self.wbesDf[validContractIds]

        self.filteredNoarDf.insert(0, "DateKey", dateKey)  
        # self.filteredWbesDf.insert(0, "DateKey", dateKey) 
        self.filteredNoarDf.insert(1, "BlockNo", list(range(1, 97)) )
        # self.filteredWbesDf.insert(1, "BlockNo", list(range(1, 97)) ) 
        # print(self.filteredNoarDf)
        # print(self.filteredWbesDf)

    def generateContractDetails(self):

        contractDetailsDict = {}
        contractDetailsDf = self.filteredNoarDf.iloc[0:11]
        for col in contractDetailsDf.columns:
            contractDetailsDict[col]= contractDetailsDf[col].tolist()
        return contractDetailsDict

    def doAll(self, dateKey:str):
        self.generateFilteredNoarWbesDf(dateKey)
        # contractDetailsDict = self.generateContractDetails()
        # print(contractDetailsDict)