# orangedatatools

![PyPI Version](https://img.shields.io/pypi/v/orangedatatools)

Python-клиент для API OrangeData: фискализация чеков, коррекций и кодов маркировки.


## Installation

```bash
pip install orangedatatools
```

## Get Started


```python
from orangedatatools.client import OrangeDataClient
from orangedatatools.schemas import ClientArgs

client = OrangeDataClient(
    org_params=ClientArgs(inn="...", group="Main", key="..."),
    api_url="https://apip.orangedata.ru:2443",
    key_private_path="./private_key.crt",
    client_cert_path="./client.crt",
    client_key_path="./client.key",
)
```
Полный пример со всеми операциями смотрите в
[`examples/get_started.py`](https://github.com/theqoocjil/orangedatatools/blob/main/examples/get_started.py)
