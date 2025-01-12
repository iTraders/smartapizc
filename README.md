<div align = "center">

# Smart API `ZC` Interface

[![Zenith Clown](https://img.shields.io/badge/🧠-Debmalya_Pramanik-blue?style=plastic)](https://zenithclown.github.io/)
[![LICENSE](https://img.shields.io/badge/⚖-LICENSE-blue?style=plastic)](https://github.com/iTraders/smartapizc/blob/master/LICENSE.md)
[![DISCLAIMER](https://img.shields.io/badge/⚠-DISCLAIMER-red?style=plastic)](https://github.com/iTraders/smartapizc/blob/master/DISCLAIMER.md)
[![GitHub Stars](https://img.shields.io/github/stars/iTraders/smartapizc?style=plastic)](https://github.com/iTraders/smartapizc/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/iTraders/smartapizc?style=plastic)](https://github.com/iTraders/smartapizc/network)
[![GitHub Issues](https://img.shields.io/github/issues/iTraders/smartapizc?style=plastic)](https://github.com/iTraders/smartapizc/issues)

</div>

<div align = "justify">

## Getting Started

```python
import pandas as pd
import smartapizc as api

# send the totp, apikey as an argument, or follow use prompt
client, session = api.client.get_client(totp = "PSPO4OGXDJTFJU5IYI7253BF34", apikey = "xJNH1Psh")

# define the interface to fetch historical Nifty50 data
interface = api.history.GetHistoricalData("NSE", "99926000")

data = interface.get(
    interval = "1M", fromdate = "2025-01-10 15:00", todate = "2025-01-10 15:30",
    client = client, rdtype = pd.DataFrame, rdtypekwargs = {"columns" : ["timestamp", "open", "high", "low", "close", "volume"]}
)

data.sample(3) # print the dataframe
```

</div>
