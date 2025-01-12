# -*- encoding: utf-8 -*-

"""
Base Class Defineation to Fetch Historical Data
"""

import datetime as dt

from typing import Iterable
from abc import ABC, abstractmethod

class HistoricalAPIBase(ABC):
    """
    The Base Class Defination to Fetch Historical Data

    The Smart API application must allow the endpoints to fetch the
    historical data for a symbol token from the exchange. The base
    class provides value assertion and time period assertion before
    sending a request to the API.

    The class is defined in a manner that an object can be defined for
    a particular symbol and all related data for the interval can be
    iteratively fetched using the :func:`.get()` method defined under
    the child class (since there is a limitation to the number of days
    that can be fetched in a single request, based on interval).
    """

    def __init__(self, exchange : str, symboltoken : str, cls : object) -> None:
        self.exchange = self.assertvalues(
            prefix = "Exchange", value = exchange,
            allowed = ["NSE", "NFO", "BSE", "BFO", "MCX", "CDS"]
        )

        self.symboltoken = symboltoken

        # ! enforce that all the child class follow the abstract directive
        assert issubclass(cls, HistoricalAPIBase)


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


    @classmethod
    def __subclasshook__(cls, subclass):
        """
        The Subclass Hook to Check if the Class is Subclass

        The default behavior of the subclasshook is to check if a
        class is a subclass of the parent class. The method is
        modified to enforce that the abstract method signature of the
        parent class is implemented in the subclass, else returns
        a signature error for the child class.

        .. code-block:: python

            @classmethod
            def __subclasshook__(cls, subclass):
                # default signature of the subclasshook
                return super().__subclasshook__(subclass)

        The method is strictly for development and debugging purposes,
        and any error raised from this class should be considered as
        a programming error for the methods in child class.
        """

        from smartapizc.errors.developer import SignatureError

        assert cls is HistoricalAPIBase, \
            "The SubclassHook is only for HistoricalAPIBase Class."
        
        slfclassdict = cls.__mro__[0].__dict__
        subclassdict = subclass.__mro__[0].__dict__

        selfabstractmethods = cls.__abstractmethods__

        for name, method in slfclassdict.items():
            # ensure only if it is an abstract method, and
            # if the abstract method has a valid signature
            if name in selfabstractmethods and hasattr(method, "__annotations__"):
                if (name not in subclassdict) \
                    or (subclassdict[name].__annotations__ != slfclassdict[name].__annotations__):
                    raise SignatureError(
                        psignature = slfclassdict[name].__annotations__,
                        csignature = subclassdict[name].__annotations__
                    )
                else:
                    continue
            else:
                continue

        return True

    @abstractmethod
    def get(
        self,
        interval : str,
        fromdate : str | dt.date | dt.datetime,
        todate : str | dt.date | dt.datetime,
        **kwargs
    ) -> Iterable:
        """
        The Abstract Method Defination to Fetch Historical Data

        The abstract method with the signature is defined under the
        parent class. The parent class also during initialization
        validates the child class :func:`.get()` method signature with
        the parent class and raises an error if the signature does not
        match. The signature considers all the arguments and return
        type to be preserved in the child class, but does not have a
        restrictions with the keyword arguments.
        """

        pass
