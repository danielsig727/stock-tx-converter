from dataclasses import dataclass
import datetime
from typing import Generator, Iterator, Optional
import re
import dateparser


@dataclass
class TDASgTradeCfm:
    # Date	Transaction Id	Symbol	Qty	B/S	Commission	Price	Principal	Net Amt
    date: datetime.date
    tx_id: str
    symbol: str
    qty: int
    op: str  # "Buy", "Sell"
    commission: float
    price: float
    principal: float
    net_amt: float


_date_pattern = re.compile(r"^\d{2}/\d{2}/\d{4}$")


def _is_date(s: str) -> bool:
    """
    check if it's `02/12/2021` format
    """
    return _date_pattern.match(s) is not None


def _parse_date(d: str) -> datetime.date:
    return dateparser.parse(d, settings={"DATE_ORDER": "MDY"}).date()


def _load_trade_cfm(line: str) -> Optional[TDASgTradeCfm]:
    tokens = line.split("\t")
    if len(tokens) == 0:
        return None
    if not _is_date(tokens[0]):
        return None

    return TDASgTradeCfm(
        date=_parse_date(tokens[0]),
        tx_id=tokens[1],
        symbol=tokens[2],
        qty=int(tokens[3]),
        op="Buy" if tokens[4] == "Bought" else "Sell",
        commission=float(tokens[5].replace(',', '')),
        price=float(tokens[6].replace(',', '')),
        principal=float(tokens[7].replace(',', '')),
        net_amt=float(tokens[8].replace(',', '')),
    )


def load_trade_cfms(lines: Iterator[str]) -> Generator[TDASgTradeCfm, None, None]:
    for l in lines:
        parsed = _load_trade_cfm(l)
        if parsed is None:
            continue
        yield parsed


if __name__ == "__main__":
    with open("tda_sg_web.txt", "r") as f:
        for e in load_trade_cfms(f):
            print(e)
