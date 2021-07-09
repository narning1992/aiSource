#!/usr/bin/env python3
import sys
import argparse
import pickle

import xgboost
import numpy as np
import pandas as pd


def load_data(input_data):
    # load input cgMLST from tsv
    data = pd.read_csv(input_data, sep="\t", header=0)

    # check if id column is in the data
    if "id" not in data.columns:
        print("ERROR\n No id column in data can't process the input. \nEXITING")
        sys.exit()
    else:
        labels = data["id"]
    # look for cgMLST columns
    data = data.fillna(-1)
    cgmlst_columns = [col for col in data if col.startswith('CAMP')]

    data = data[cgmlst_columns]

    # Find columns which have double alleles as indicated by a semicolon then
    # replace those with NAs
    columns_with_semicolon = data.columns[np.where(data.dtypes==object)[0]]
    for col in columns_with_semicolon:
        data[col] = pd.to_numeric(data[col], downcast="integer",errors="coerce")
    data.fillna(-1, inplace=True)

    # check if we have all 1343 cgMLST loci
    if len(cgmlst_columns) < 1343:
        print("""ERROR\n
              Could not find 1,343 loci in the cgMLST data.
              cgMLST loci start with CAMP in the pubmlst output data\n
              EXITING""")
        sys.exit()
    return(labels, data.astype(int))


def make_predictions(model,  data):
    # make predictions using the loaded XGBoost model

    # define our source labels
    source_dict = {
        0: "cattle",
        1: "chicken",
        2: "environment",
        3: "bird",
        4: "sheep"
        }

    # make probabilistic assignment over all sources
    source_prob = model.predict_proba(data)

    # get highest probability
    source_pred = list(np.argmax(source_prob, axis=1))
    source_pred = [source_dict[x] for x in source_pred]
    source_prob = list(source_prob.T)

    # get headers for output
    headers = ["probability_{}".format(source_dict[x]) for x in range(5)]

    return (headers, source_pred, source_prob)


def main():
    # Script to use aiSource to attribue the source of human campylobacter
    # infection based on the publication "Machine learning to predict the
    # source of campylobacteriosis using whole genome data"

    # read in command line arguments
    parser = argparse.ArgumentParser(
        description='aiSource source attribution of campylobacter cgMLSTs')
    parser.add_argument('-i', type=str, help='dataset to be classified')
    parser.add_argument(
        '-n',
        default="placeholder",
        type=str,
        help='give the output a prefix')
    args = parser.parse_args()

    # check if an output prefix has been specified if not take the input data
    # as prefix
    if args.n == "placeholder":
        prefix = args.i.split(".")[0]
    else:
        prefix = args.n

    print("Predicting the source on the file {} output will be stored in {}_aiSource_out.tsv".format(args.i, prefix))

    # load in data which as it is downloaded from pubMLST
    label, data = load_data(args.i)

    # load in the trained XGBoost classifier
    model=pickle.load(open('./aiSource_classifier_object.p', 'rb'))

    # make predictions
    headers, source_pred, source_probs=make_predictions(model, data)

    # put prediction into dataframe for outputting
    content_df=[list(label), list(source_pred)]
    content_df += [ list(x) for x in source_probs]
    column_headers=["id", "predicted_source"]
    column_headers += headers
    df=pd.DataFrame(dict(zip(column_headers, content_df))).round(decimals=3)

    # output dataframe
    df.to_csv("{}_aiSource_out.tsv".format(prefix), sep="\t", index=False)


if __name__ == "__main__":
    main()
