# Imports

import pandas as pd
import xgboost as xgb
import bentoml

# Importing The data
raw_df = pd.read_csv("all_songs.csv")

columns = ['danceability', 'energy', 'key', 'mode', 'speechiness', 'acousticness',
           'instrumentalness', 'liveness', 'valence', 'loudness', 'tempo', 'duration_ms',
           'time_signature', 'chorus_hit', 'sections', 'target']

df_full_train = df[columns].reset_index(drop=True)

y_full_train = df.target.values

del df_full_train['target']

df_train = df_train.loc[:, ~df_train.columns.duplicated()]
df_test = df_test.loc[:, ~df_test.columns.duplicated()]
df_val = df_val.loc[:, ~df_val.columns.duplicated()]

dfulltrain = xgb.DMatrix(df_train, label=y_train)

dtest = xgb.DMatrix(df_test)

xgb_params = {
    'eta': 0.1,
    'max_depth': 6,
    'min_child_weight': 10,

    'objective': 'binary:logistic',
    'eval_metric': 'auc',

    'nthread': 8,
    'seed': 1,
    'verbosity': 1,
}

model = xgb.train(xgb_params, dfulltrain, num_boost_round=175)

y_pred = model.predict(dtest)

bentoml.xgboost.save_model('spotify_hit_model', model)
