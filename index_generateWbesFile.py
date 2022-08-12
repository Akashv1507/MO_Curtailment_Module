from src.appConfig import loadAppConfig
import datetime as dt
import argparse
import os
import pandas as pd




appConfig = loadAppConfig()

endDate = dt.datetime.now()
# startDate = endDate - timedelta(days=2)
startDate = endDate

# get start and end dates from command line
parser = argparse.ArgumentParser()
parser.add_argument('--start_date', help="Enter Start date in yyyy-mm-dd format",
                    default=dt.datetime.strftime(startDate, '%Y-%m-%d'))
parser.add_argument('--end_date', help="Enter end date in yyyy-mm-dd format",
                    default=dt.datetime.strftime(endDate, '%Y-%m-%d'))

                    
args = parser.parse_args()
startDate = dt.datetime.strptime(args.start_date, '%Y-%m-%d')
endDate = dt.datetime.strptime(args.end_date, '%Y-%m-%d')

startDate = startDate.replace(hour=0, minute=0, second=0, microsecond=0)
endDate = endDate.replace(hour=0, minute=0, second=0, microsecond=0)

print('startDate = {0}, endDate = {1}'.format(dt.datetime.strftime(
    startDate, '%Y-%m-%d'), dt.datetime.strftime(endDate, '%Y-%m-%d')))

startDateStr= dt.datetime.strftime(startDate, '%d%m%y')
endDateStr= dt.datetime.strftime(endDate, '%d%m%y')

wbesRawFilesPath = appConfig['WbesRawFolderPath']
wbesDerivedFilesPath = appConfig['WbesDerivedFolderPath']
dumpFileName = f'{wbesDerivedFilesPath}STOA-{startDateStr}-{endDateStr}.csv' 

allWbesFiles  = os.listdir(wbesRawFilesPath)

wbesFilePath=''
for wbesFile in allWbesFiles:
        if (startDateStr in wbesFile) or (endDateStr in wbesFile):
            wbesFilePath = wbesRawFilesPath + wbesFile
            break
# read wbes file only if wbesfilePath is not null and noarfile reading is successfull
if wbesFilePath!='' :
    wbesDf = pd.read_csv(wbesFilePath)
    wbesDf = wbesDf.drop(['APPLICANT', 'FROM STATE', 'FROM UTILITY', 'TO STATE', 'TO UTILITY', 'LINK NAME', 'OTHER REGION', 'Total'], axis=1)
    wbesDf = wbesDf.loc[:, ~wbesDf.columns.str.contains('^Unnamed')]
    tbList = list(range(1,97))
    approvalId = wbesDf['APPROVAL NO'].unique()
    colName = ['DATE', 'BLK' , *approvalId]
    transposeWbesDf = pd.DataFrame(columns=colName)
    # print(len(wbesDf['APPROVAL NO'].unique()))
    groupWbesObj = wbesDf.groupby('DATE')

    for date, groupWbesDf in groupWbesObj:
        groupWbesDf = groupWbesDf.set_index('DATE')
        groupWbesDf = groupWbesDf.set_index('APPROVAL NO').T
        groupWbesDf.reset_index(drop=True, inplace=True)
        groupWbesDf.insert(0, 'BLK', tbList)
        groupWbesDf.insert(0, 'DATE', date)
        transposeWbesDf = pd.concat((transposeWbesDf,groupWbesDf ))
    
    transposeWbesDf['DATE'] = pd.to_datetime(transposeWbesDf['DATE'], dayfirst=True)
    transposeWbesDf = transposeWbesDf[(transposeWbesDf['DATE']>= startDate) & (transposeWbesDf['DATE']<= endDate)]
    transposeWbesDf['DATE'] = transposeWbesDf['DATE'].apply(lambda x: dt.datetime.strftime(x, '%Y-%m-%d'))
    transposeWbesDf.to_csv(dumpFileName, index=False)
    



    
    
    