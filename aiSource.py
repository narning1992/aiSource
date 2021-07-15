#!/usr/bin/env python3
import sys
import argparse
import pickle
from collections import Counter

import xgboost
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.metrics import classification_report


def load_data(input_data, retrain_flag):
    # load input cgMLST from tsv
    data = pd.read_csv(input_data, sep="\t", header=0)

    # check if id column is in the data
    if "id" not in data.columns:
        print("ERROR\n No id column in data can't process the input. \nEXITING")
        sys.exit()
    # look for cgMLST columns
    cgmlst_columns = [col for col in data if col.startswith('CAMP')]
    cgmlst_columns += ["id"]

    # look whether we are retraining and retain the column on which we're
    # retraining
    if retrain_flag:
        cgmlst_columns += [retrain_flag]
    data = data[cgmlst_columns]

    # Find columns which have double alleles as indicated by a semicolon then
    # replace those with NAs
    columns_with_semicolon = data.columns[np.where(data.dtypes == object)[0]]
    for col in columns_with_semicolon:
        if col != "id" and col != retrain_flag:
            data[col] = pd.to_numeric(
                data[col],
                downcast="integer",
                errors="coerce")

    # drop rows with more than 10% missingness
    before = data.shape[0]
    data.dropna(thresh=134, axis=0, inplace=True)
    print(
    "Dropped {} rows because over 10% missingness. These won't show up in the output".format(
        before -
        data.shape[0]))
    data.fillna(-1, inplace=True)

    # get ids
    ids = data["id"]
    data.drop("id", axis=1, inplace=True)

    if retrain_flag:
        print("Retraining classifier with the label: {}".format(retrain_flag))
        # get labels for retraining
        labels = data[retrain_flag]
        if len(set(labels)) <= 1:
            print("ERROR\nThere is only one category in the label columns\nEXITING")
            sys.exit()
        # throw out labels with too gewe members
        label_counts = dict(Counter(labels))
        for label, label_count in label_counts.items():
            if label_count <= 15:
                print(
    "Removing all samples with the label {} as there are only {} of them".format(
        label, label_count))
                data = data[data[retrain_flag] != label]
        labels = data[retrain_flag]

        data.drop(retrain_flag, axis=1, inplace=True)

    else:
        labels = None

    # check if we have all 1343 cgMLST loci
    if len(cgmlst_columns) < 1343:
        print("""ERROR\n
              Could not find 1,343 loci in the cgMLST data.
              cgMLST loci start with CAMP in the pubmlst output data\n
              EXITING""")
        sys.exit()

    return(ids, data.astype(int), labels)


def retrain_clf(model, data, labels):
    print("refitting model")

    # encode lables as integers first then one-hot encode (dummy variable)
    encoder = LabelEncoder()
    labels = encoder.fit_transform(labels).reshape(-1, 1)
    labels = OneHotEncoder(sparse=False).fit_transform(labels)
    label_dict = dict(zip(range(len(encoder.classes_)), encoder.classes_))

    # split randomly into training and testing
    data_train, data_test, labels_train, labels_test = train_test_split(
        data,
        labels,
        test_size=0.25,
        stratify=labels)
    model.fit(data_train, labels_train)
    labels_predict = model.predict(data_test)

    # get accuracy
    print("Accuracy of the retrained model based on random 25% testing split")
    accuracy_report = classification_report(
            labels_test,
            labels_predict,
            target_names=label_dict.values())
    print(accuracy_report)
    print("Now retraining with the whole data")
    model.fit(data, labels)
    print("Finished training")
    return((label_dict, model), accuracy_report)


def make_predictions(model,  data, label_dict):
    # make predictions using the loaded XGBoost model

    # make probabilistic assignment over all sources
    source_prob=model.predict_proba(data)

    # get highest probability
    source_pred=list(np.argmax(source_prob, axis = 1))
    source_pred=[label_dict[x] for x in source_pred]
    source_prob=list(source_prob.T)

    # get headers for output
    headers=[
        "probability_{}".format(label_dict[x])
        for x in range(len(label_dict.keys()))]

    return (headers, source_pred, source_prob)


def main():
    # Script to use aiSource to attribue the source of human campylobacter
    # infection based on the publication "Machine learning to predict the
    # source of campylobacteriosis using whole genome data"

    # read in command line arguments
    parser=argparse.ArgumentParser(
        description='aiSource source attribution of campylobacter cgMLSTs')
    parser.add_argument(
        '-i',
        '--input',
        type=str,
        help='dataset to be classified')
    parser.add_argument(
        '-n', '--name',
        default=None,
        type=str,
        help='give the output a prefix')
    parser.add_argument(
        '-rt', '--retrain', default=None, type=str,
        help='flag for retraining the classifier. Specify which column to train on')
    parser.add_argument(
        '-clf', '--classifier',
        default="aiSource_classifier_object.p",
        type=str,
        help='''classifier object to do the prediction. Default is the aiSource predictor,
        but if you have retrained the classifier with the rt flag you can specify
        the resulting object here and use it for prediction''')

    args=parser.parse_args()

    # check if an output prefix has been specified if not take the input data
    # as prefix
    if args.name:
        prefix=args.name
    else:
        prefix=args.input.split(".")[0]

    print(
        "Predicting the source on the file {} output will be stored in {}_aiSource_out.tsv".format(
            args.input,
            prefix))

    # load in data which as it is downloaded from pubMLST
    ids, data, labels=load_data(args.input, args.retrain)

    # load in the trained classifier

    if args.retrain:
        # get initial classifier and retrain
        label_dict, model=pickle.load(
            open("aiSource_classifier_object.p", 'rb'))
        new_model, accuracy_report=retrain_clf(model, data, labels)
        with open("{}_retraining_accurary_report.txt".format(prefix), "w+") as outf:
            outf.write(accuracy_report)

        out_pickle="{}_retrained_clf.p".format(args.name)
        print("""Dumping retrained classifier in {}\n If you want to use this
              for prediction specify this object in the -clf flag in a rerun of
              aisource""".format(out_pickle))
        pickle.dump(new_model, open(out_pickle, "wb"))
        print("DONE.EXITING")

    else:
        label_dict, model=pickle.load(open(args.classifier, 'rb'))
        # make predictions
        headers, source_pred, source_probs=make_predictions(
            model, data, label_dict)

        # put prediction into dataframe for outputting
        content_df=[list(ids), list(source_pred)]
        content_df += [list(x) for x in source_probs]
        column_headers=["id", "prediction"]
        column_headers += headers
        df=pd.DataFrame(
            dict(zip(column_headers, content_df))).round(
            decimals=3)

        # output dataframe
        df.to_csv("{}_aiSource_out.tsv".format(prefix), sep="\t", index=False)
        print("DONE.EXITING")


if __name__ == "__main__":
    main()
