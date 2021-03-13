import tx_converter.tda_stmt as td_stmt
import tx_converter.stockscafe as stockscafe
import tx_converter.util as util

if __name__ == "__main__":
    path = "td_all.txt"

    sc_txs = []
    with open(path, "r") as f:
        for tda_tx in td_stmt.load_stmt_from_text(f):
            sc_tx = stockscafe.from_tda_stmt_tx(tda_tx)
            if sc_tx is None:
                continue
            sc_txs.append(sc_tx)

    with open("tda_stockscafe.csv", "w") as f:
        util.write_dataclass_csv(sc_txs, f)
