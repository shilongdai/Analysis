import dill
import numpy as np
import pandas as pd


categories = [
    'air.level', 'base.num', 'busi.level', 'has.covered', 'has.garage',
    'has.lot', 'has.street', 'neighborhood', 'pet.allowed',
    'traffic.level', 'has.parking', 'has.pub.elementary',
    'has.priv.elementary', 'has.pub.mid', 'has.cha.high',
    'has.priv.high', 'count.pub.high', 'pub.elt.mid',
    'priv.elt.mid', 'has.cha.mid.high', 'has.priv.mid.high', 'has.pub.mid.high',
    'priv.el.hi', 'cha.elt.mid.hi', 'priv.elt.mid.hi', "zip"
]


if __name__ == "__main__":
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    with open("final_sqft_mod.joblib", "rb") as file:
        sqft_mod = dill.load(file)
    sqft_df = pd.read_csv("fill_sqft.csv", low_memory=False)
    full_df = pd.read_csv("full.csv", low_memory=False)
    sqft_df = pd.get_dummies(sqft_df, columns=categories)

    sqft_df_tofill = sqft_df.loc[full_df["sqft.regressed"], sqft_mod.feature_names_in_]
    print(sqft_mod.predict(sqft_df_tofill))
    full_df.loc[full_df["sqft.regressed"], "sqft"] = sqft_mod.predict(sqft_df_tofill)

    full_df.to_csv("full_sqft.csv", index=False)
