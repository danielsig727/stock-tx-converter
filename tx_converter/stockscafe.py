from dataclasses import dataclass
from tx_converter.firstrade_cfm import FirstradeCfm
from typing import Optional
import datetime

from .tda_stmt import TDAStmtTransaction
from .tda_sg import TDASgTradeCfm


@dataclass
class StocksCafeTransaction:
    op: str  # "Buy", "Sell", "Fees"
    exchange_code: str  # Exchange Code (i.e. SGX or HKEX)
    symbol: str  # Symbol
    qty: int  # Units Purchased or Sold
    currency: str
    price: float  # Price Paid or Received (based on the currency this stock trades in)
    date: str  # Date of transaction (YYYY-MM-DD or MM/DD/YYY)
    amount_after_fee: Optional[
        float
    ]  # Total after fees (based on the currency this stock trades in)
    notes: Optional[str]


def from_tda_stmt_tx(tx: TDAStmtTransaction) -> Optional[StocksCafeTransaction]:
    if tx.op not in ("Buy", "Sell"):
        return None

    return StocksCafeTransaction(
        op=tx.op,
        exchange_code="USX",
        symbol=tx.symbol_cusip,
        qty=tx.qty,
        currency="USD",
        price=tx.price,
        date=tx.trade_date.strftime("%Y-%m-%d"),
        amount_after_fee=tx.amount,
        notes="",
    )


def from_tda_sg_trade_cfm(tx: TDASgTradeCfm) -> Optional[StocksCafeTransaction]:
    return StocksCafeTransaction(
        op=tx.op,
        exchange_code="USX",
        symbol=tx.symbol,
        qty=tx.qty,
        currency="USD",
        price=tx.price,
        date=tx.date.strftime("%Y-%m-%d"),
        amount_after_fee=tx.net_amt,
        notes=f"converted from tda_sg_trade_cfm ({datetime.datetime.now().isoformat(timespec='seconds')})",
    )


def from_firstrade_cfm(tx: FirstradeCfm) -> Optional[StocksCafeTransaction]:
    if tx.op not in ("Buy", "Sell"):
        return None

    return StocksCafeTransaction(
        op=tx.op,
        exchange_code="USX",
        symbol=tx.symbol,
        qty=tx.qty,
        currency="USD",
        price=tx.price,
        date=tx.date.strftime("%Y-%m-%d"),
        amount_after_fee=tx.amount,
        notes=f"converted from firstrade_cfm ({datetime.datetime.now().isoformat(timespec='seconds')})",
    )
