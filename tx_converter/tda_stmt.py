from typing import Generator, Iterable, Iterator, Optional
import re
import dateparser
import datetime

from dataclasses import dataclass


def _starts_with_date(s: str) -> bool:
    """
    simply check if the lines starts like: something/something/something
    """
    tokenized = s.split(" ")
    if len(tokenized) == 0:
        return False
    date = tokenized[0]
    return len(date.split("/")) == 3


def preprocess_stmt(lines: Iterator[str]) -> Generator[str, None, None]:
    curr_line = None
    for line in lines:
        if _starts_with_date(line):
            if curr_line:
                yield curr_line

            curr_line = line.rstrip()
        else:
            if not curr_line:
                curr_line = line.rstrip()
            else:
                curr_line += " " + line.rstrip()

    if curr_line:
        yield curr_line


trading_tx_pattern = re.compile(
    r"^(?P<trade_date>[\d/]+) (?P<settle_date>[0\d/]+) "
    r"(?P<acc_type>\w+) ((?P<op>[^\s]+) )?- "
    r"(?P<activity>([A-Z][a-z]+\s?){1,2}) "
    r"(?P<description>[A-Z].+?)"
    r"( (?P<fee_type>\w+) Fee (?P<fee>[\d\.,]+))*"
    r"( Payable: (?P<payable>[\d/]+))*"
    r"( (?P<dividend_type>\w+) Dividends (?P<dividends>[\d\.,]+))* "
    r"(?P<symbol_cusip>[A-Z0-9\-]+) "
    r"(?P<qty>[\d,\-]+) (?P<price>[\d\.,]+) "
    r"(?P<amount>\(?[\d\.,]+\)?) (?P<balance>[\d\.,\s]+)\s*$"
)


@dataclass
class TDAStmtTransaction:
    trade_date: datetime.date
    settle_date: datetime.date
    acc_type: str
    op: Optional[str]  # "Buy", "Sell", "Div/Int", "Journal"
    activity: str
    description: str

    fee_type: Optional[str]
    fee: Optional[float]

    payable: Optional[datetime.date]

    dividend_type: Optional[str]
    dividends: Optional[float]

    symbol_cusip: Optional[str]
    qty: Optional[int]
    price: float
    amount: float
    balance: float


def _parse_date(d: str) -> datetime.date:
    return dateparser.parse(d, settings={"DATE_ORDER": "MDY"}).date()


def _parse_int(s: str, parse_neg: bool = False) -> int:
    """
    input like "123-" will be 123
    """
    parsed = int(s.replace(",", "").replace("-", ""))
    if parse_neg and (s.startswith("-") or s.endswith("-")):
        return -parsed
    return parsed


def _parse_float(s: str, parse_neg: bool = False) -> float:
    """
    input like "(123)" will be -123
    """
    parsed = float(s.replace(",", "").replace("(", "").replace(")", ""))
    if parse_neg and s.startswith("("):
        return -parsed
    return parsed


def parse_transaction(line: str) -> Optional[TDAStmtTransaction]:
    match = trading_tx_pattern.match(line)
    if not match:
        return None

    return TDAStmtTransaction(
        trade_date=_parse_date(match.group("trade_date")),
        settle_date=_parse_date(match.group("settle_date")),
        acc_type=match.group("acc_type"),
        op=match.group("op") if match.group("op") else None,
        activity=match.group("activity"),
        description=match.group("description"),
        fee_type=match.group("fee_type") if match.group("fee_type") else None,
        fee=_parse_float(match.group("fee")) if match.group("fee_type") else None,
        payable=_parse_date(match.group("payable")) if match.group("payable") else None,
        dividend_type=match.group("dividend_type")
        if match.group("dividend_type")
        else None,
        dividends=_parse_float(match.group("dividends"))
        if match.group("dividend_type")
        else None,
        symbol_cusip=match.group("symbol_cusip")
        if match.group("symbol_cusip") != "-"
        else None,
        qty=_parse_int(match.group("qty")) if match.group("qty") != "-" else None,
        price=_parse_float(match.group("price")),
        amount=_parse_float(match.group("amount")),
        balance=_parse_float(match.group("balance")),
    )


def load_stmt_from_text(lines: Iterable[str]) -> Iterable[TDAStmtTransaction]:
    for line in preprocess_stmt(lines):
        parsed = parse_transaction(line)
        if parsed is None:
            continue
        yield parsed


if __name__ == "__main__":
    with open("td_all.txt", "r") as f:
        for e in load_stmt_from_text(f):
            print(e)
