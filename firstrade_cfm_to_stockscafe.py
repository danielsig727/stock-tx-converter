import tx_converter.firstrade_cfm as firstrade_cfm
import tx_converter.stockscafe as stockscafe
import tx_converter.util as util

if __name__ == "__main__":
    path = "firstrade_cfm.txt"

    sc_txs = []
    with open(path, "r") as f:
        for tda_tx in firstrade_cfm.load_stmt_from_text(f):
            sc_tx = stockscafe.from_firstrade_cfm(tda_tx)
            if sc_tx is None:
                continue
            sc_txs.append(sc_tx)

    with open("firstrade_cfm_stockscafe.csv", "w") as f:
        util.write_dataclass_csv(sc_txs, f)
