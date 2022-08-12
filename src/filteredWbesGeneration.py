from typing import List
import pandas as pd
import datetime as dt

class FilteredWbesCalculator():
    """ class to calculate filtered WBES dataframe
    """

    def __init__(self, wbesFilePath:str ):
        """ constructor method 

        Args:
            wbesFilePath (str):  WBES file path for initialization of WBES Dataframe for whole month.
        """  
        self.wbesDf = pd.read_csv(wbesFilePath, dtype='unicode')
        # self.wbesDf = self.wbesDf.iloc[1:, :]
        # self.wbesDf.reset_index(drop=True, inplace=True)
        # self.wbesDf.rename(columns={self.wbesDf.columns[0]:'DATE', self.wbesDf.columns[1]:'BLK'}, inplace=True)
       
                                 
    def generateFilteredWbesDf(self, startDate:dt.datetime, endDate:dt.datetime, validContIdsMonth:List)->pd.DataFrame:
        """method to generate WBES filtered Dataframe

        Args:
            startDate (dt.datetime): startDate
            endDate (dt.datetime): endDate
            validContIdsMonth (List): valid contract IDs list for entire month since WBES excel is for entire month

        Returns:
            pd.DataFrame: return filtered WBES Dataframe for entire month
        """        
        # print(len(validContIdsMonth))
        wbesValidContIds = []
        remainingWbesContIds=[]
        wbesCols = self.wbesDf.columns.tolist()
        for contIds in validContIdsMonth:
            if contIds in wbesCols:
                wbesValidContIds.append(contIds)
            else:
                remainingWbesContIds.append(contIds)
        filteredWbesDf = self.wbesDf[["DATE", 'BLK']+ wbesValidContIds]
        # print(filteredWbesDf)
        cols = filteredWbesDf.columns.tolist()[1:]
        for col in cols :
            filteredWbesDf[col] = filteredWbesDf[col].astype('float')  

        filteredWbesDf['DATE'] = pd.to_datetime(filteredWbesDf['DATE'], dayfirst=True)
        filteredWbesDf = filteredWbesDf[(filteredWbesDf['DATE']>= startDate) & (filteredWbesDf['DATE']<= endDate)]
        filteredWbesDf['DATE'] = filteredWbesDf['DATE'].apply(lambda x: dt.datetime.strftime(x, '%Y-%m-%d'))
        return filteredWbesDf
        # return {'filteredWbesDf':filteredWbesDf, 'remainingWbesContIds':remainingWbesContIds}