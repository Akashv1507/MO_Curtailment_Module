from src.appConfig import loadAppConfig
import datetime as dt
import argparse
from src.curtailmentCalculator import calculateCurtailment
import warnings

warnings.simplefilter('ignore')
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


calculateCurtailment(startDate, endDate, appConfig)