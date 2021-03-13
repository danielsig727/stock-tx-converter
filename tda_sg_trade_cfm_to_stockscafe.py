import tx_converter.tda_sg as tda_sg
import tx_converter.stockscafe as stockscafe
import tx_converter.util as util

if __name__ == "__main__":
    path = "tda_sg_web.txt"

    sc_txs = []
    with open(path, "r") as f:
        for tda_sg_cfm in tda_sg.load_trade_cfms(f):
            sc_tx = stockscafe.from_tda_sg_trade_cfm(tda_sg_cfm)
            if sc_tx is None:
                continue
            sc_txs.append(sc_tx)

    with open("tda_sg_stockscafe.csv", "w") as f:
        util.write_dataclass_csv(sc_txs, f)
