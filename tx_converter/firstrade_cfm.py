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


@dataclass
class FirstradeCfm:
    date: datetime.date
    op: str  # "Buy", "Sell", "Deposit"
    qty: Optional[int]  # always positive
    description: str
    symbol: Optional[str]
    acct_type: str
    price: Optional[float]
    amount: float  # always positive


def _parse_date(d: str) -> datetime.date:
    return dateparser.parse(d, settings={"DATE_ORDER": "MDY"}).date()


def parse_transaction(line: str) -> Optional[FirstradeCfm]:
    if not _starts_with_date(line):
        return None

    tokens = line.split("\t")
    if len(tokens) != 8:
        print(len(tokens))
        return None

    op_map = {
        "Bought": "Buy",
        "Sold": "Sell",
    }
    return FirstradeCfm(
        date=_parse_date(tokens[0]),
        op=op_map.get(tokens[1], tokens[1]),
        qty=None if tokens[2] == "" else abs(int(tokens[2])),
        description=tokens[3],
        symbol=None if tokens[2] == "" else tokens[4],
        acct_type=tokens[5],
        price=None if tokens[2] == "" else float(tokens[6]),
        amount=abs(float(tokens[7].split(" ")[0])),
    )


def load_stmt_from_text(lines: Iterable[str]) -> Generator[FirstradeCfm, None, None]:
    for line in preprocess_stmt(lines):
        parsed = parse_transaction(line)
        if parsed is None:
            continue
        yield parsed


if __name__ == "__main__":
    with open("firstrade_cfm.txt", "r") as f:
        for e in load_stmt_from_text(f):
            print(e)
