# -*- encoding: utf-8 -*-

"""
Get Historical Data for a Symbol Token
"""

import datetime as dt
from typing import Iterable

from smartapizc.history.base import HistoricalAPIBase

class GetHistoricalData(HistoricalAPIBase):
    """
    Class Implementation to Fetch Historical Data for a Symbol Token

    The class is used to fetch historical data for a symbol token from
    the exchange. The data is fetched based on the interval and the
    number of days requested.

    .. note::

        There is a limitation to the number of days that can be fetched
        in a single request, based on the interval. The development is
        in progress to fetch the data for a longer period iteratively,
        by breaking the days into smaller chunks.

    :type  exchange: str
    :param exchange: The exchange for which the data is to be fetched.
        The exchange can be one of the following - "NSE", "NFO", "BSE",
        "BFO", "MCX", "CDS".

    :type  symboltoken: str
    :param symboltoken: The symbol token for which the data is to be
        fetched. The symbol token is a unique identifier for a stock
        in the exchange. The list of valid symbol tokens can be fetched
        from https://margincalculator.angelbroking.com/.

    .. note::

        The symbol token for a stock will remain the same, however
        the symbol token for NFO/BFO/FNO will change based on the
        expiry and thus an exhaustive valid list is impossible to be
        defined.

    .. important::

        The original API (https://smartapi.angelbroking.com/docs)
        fails without a method to catch the error when the symbol is
        invalid. Currently, this is under development.
    """

    def __init__(self, exchange : str, symboltoken : str) -> None:
        super().__init__(exchange, symboltoken, cls = GetHistoricalData)


    def makeparams(self, interval : str, fromdate : str, todate : str) -> dict:
        """
        Make the Parameters for Fetching the Historical Data

        The method is used to make the parameters for fetching the
        historical data. The parameters are defined based on the
        interval, from date, and to date.

        :type  interval: str
        :param interval: The interval for fetching the data. Valid
            arguments (long, original form) can be found at
            https://smartapi.angelbroking.com/docs/Historical. In
            addition, the :mod:`smartapizc` introduces short hand
            notation like "1M", "3M", "5M", "10M", "15M", "30M", "1H",
            or "1D" for the same and is internally converted.

        :type  fromdate, todate: str
        :param fromdate, todate: The start and the end date for which
            the data is to be fetched. The date should be in the format
            of a string in the format "YYYY-MM-DD".
        """

        return {
            # class objects, cannot be changed
            "exchange" : self.exchange, "symboltoken" : self.symboltoken,

            # user defined, fetched from underlying .get() method
            "interval" : interval, "fromdate" : fromdate, "todate" : todate
        }


    def get(
        self,
        interval : str,
        fromdate : str | dt.date | dt.datetime,
        todate : str | dt.date | dt.datetime,
        **kwargs
    ) -> Iterable:
        """
        Fetch Raw Historical Data for a Symbol Token
        
        For a given symbol token, define the from and to date with an
        appropriate interval to fetch the historical data. The data is
        returned in a list of list format.

        :type  interval: str
        :param interval: The interval for fetching the data. Valid
            arguments (long, original form) can be found at
            https://smartapi.angelbroking.com/docs/Historical. In
            addition, the :mod:`smartapizc` introduces short hand
            notation like "1M", "3M", "5M", "10M", "15M", "30M", "1H",
            or "1D" for the same and is internally converted.

        :type  fromdate, todate: str | dt.date | dt.datetime
        :param fromdate, todate: The start and the end date for which
            the data is to be fetched. The date can be in the format
            of a string, a  :class:`datetime.date` object, or a
            :class:`datetime.datetime` object.

        Keyword Arguments
        -----------------

        The abstract method's signature is enforced in the parent class
        and the following additional parameters are centric to the
        :class:`.GetHistoricalData` class.

            * **client** (:class:`SmartApi.SmartConnect`): The client
                object for the Smart API. The client object is used to
                fetch the data from the API.

            .. warning::

                The client object is mandatory for the function to
                work. The client object is created using the
                :func:`smartapizc.client.get_client` function. The
                future version of the module will be able to
                automatically call the client object from the defined
                environment controls.

            * **rdtype** (*object*): The return type for the data.
                The default return type is a list of list, but accepts
                [:clsss:`pd.DataFrame`, :class:`np.ndarray`] as an
                additional return type.

            * **rdtypekwargs** (*dict*): A special keyword arguments
                to control the return data type. If a specialized class
                is passed as a return type like :class:`pd.Dataframe`
                then assign pass additional control arguments to format
                the data in a desired format.

        Example Usecase(s)
        ------------------

        The :mod:`smartapizc` is a versatile module built on top of the
        :mod:`smartapi-python` module to perform actions.

        .. code-block:: python

            import smartapizc as api
            client, session = api.client.get_client() # follow prompt

            # symbol token is for Nifty 50
            symboltoken = "99926000"
            interface = api.history.GetHistoricalData("NSE", symboltoken)

            # let's define the interval and period to fetch data
            interval = "1M" # short from notation, as in module
            fromdate, todate = "2025-01-10 15:00", "2025-01-10 15:30"

            # get the data in raw format, without additional changes
            data = interface.get(interval, fromdate, todate, client = client)
            >> [
                ['2025-01-10T15:00:00+05:30', '23410.85', '23418.9', '23402.95',
                '23404.25', '0'],
                ...
            ]

            # the function also gives you the ability to return any
            # other data type format, with controls, like for example:
            data = interface.get(
                interval, fromdate, todate, client = client,
                rdtype = pd.DataFrame, rdtypekwargs = {
                    "columns" : ["timestamp", "open", "high", "low", "close", "volume"]
                }
            )


        Return Type
        -----------

        The return type is an iterable object, however the type of the
        iterable object is controllable. For example, it can be a
        :class:`np.ndarray` or :clsss:`pd.DataFrame` as per requirement.

        :rtype:  Iterable
        :return: The historical data fetched for the symbol token in
            the given interval and time period.
        """

        interval = self.setinterval(interval)
        fromdate, todate = self.asserttimeperiod(
            fromdate = fromdate, todate = todate,
            interval = interval, dtformat = "%Y-%m-%d %H:%M"
        )

        # ! keyword arguments, client is mandatory, else default
        client = kwargs.get("client", None)
        rdtype = kwargs.get("rdtype", list)

        return rdtype(
            client.getCandleData(
                self.makeparams(interval, fromdate, todate)
            )["data"],
            **kwargs.get("rdtypekwargs", dict())
        )
