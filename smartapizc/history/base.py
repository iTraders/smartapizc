# -*- encoding: utf-8 -*-

"""
Base Class Defineation to Fetch Historical Data
"""

import datetime as dt

from abc import ABC, abstractmethod

class HistoricalAPIBase(ABC):
    def __init__(
        self,
        exchange : str,
        symboltoken : str,
        interval : str,
        fromdate : str | dt.date | dt.datetime,
        todate : str | dt.date | dt.datetime,
        **kwargs
    ) -> None:
        self.exchange = self.assertvalues(
            prefix = "Exchange", value = exchange,
            allowed = ["NSE", "NFO", "BSE", "BFO", "MCX", "CDS"]
        )

        self.symboltoken = symboltoken
        self.interval = self.setinterval(interval)
        self.fromdate, self.todate = self.asserttimeperiod(
            fromdate, todate,
            interval = self.interval,
            dtformat = kwargs.get("dtformat", "%Y-%m-%d %H:%M")
        )


    @staticmethod
    def assertvalues(prefix : str, value : str, allowed : list) -> str:
        assert value in allowed, \
            f"{prefix} Value `{value}` Not in: {allowed}"

        return value


    def setinterval(self, interval : str) -> str:
        shortkey = {
            "1M" : "ONE_MINUTE",
            "3M" : "THREE_MINUTE",
            "5M" : "FIVE_MINUTE",
            "10M" : "TEN_MINUTE",
            "15M" : "FIFTEEN_MINUTE",
            "30M" : "THIRTY_MINUTE",
            "1H" : "ONE_HOUR",
            "1D" : "ONE_DAY"
        }

        allowed = list(shortkey.keys()) + list(shortkey.values())
        interval = self.assertvalues(
            prefix = "Interval", value = interval,
            allowed = allowed
        )

        return interval if interval in shortkey.values() else shortkey[interval]


    @staticmethod
    def asserttimeperiod(
        fromdate : str | dt.date | dt.datetime,
        todate : str | dt.date | dt.datetime,
        interval : str,
        dtformat : str
    ) -> tuple:
        retfromdate, rettodate = fromdate, todate
        maxdaysforinterval = {
            "ONE_MINUTE" : 30,
            "THREE_MINUTE" : 60,
            "FIVE_MINUTE" : 100,
            "TEN_MINUTE" : 100,
            "FIFTEEN_MINUTE" : 200,
            "THIRTY_MINUTE" : 200,
            "ONE_HOUR" : 400,
            "ONE_DAY" : 2000
        }

        # ? the return format has to be string, as accepted by the API
        # ! there is a limitation in max days in one request, for interval
        if isinstance(fromdate, (dt.date, dt.datetime)):
            retfromdate = retfromdate.strftime(dtformat)
        elif isinstance(fromdate, str):
            fromdate = dt.datetime.strptime(fromdate, dtformat)
        else:
            raise ValueError("From Date is not in Valid Format.")

        if isinstance(todate, (dt.date, dt.datetime)):
            rettodate = rettodate.strftime(dtformat)
        elif isinstance(todate, str):
            todate = dt.datetime.strptime(todate, dtformat)
        else:
            raise ValueError("To Date is not in Valid Format.")
        
        # calculate the different between the two dates in seconds
        diff = (todate - fromdate).total_seconds()
        assert diff <= maxdaysforinterval[interval] * 24 * 60 * 60, \
            f"Time Period Exceeds the Limit for {interval}"

        return retfromdate, rettodate
