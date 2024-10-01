#!/usr/bin/env python
'''
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
'''
import argparse
import logging
import wandb
import pandas as pd
import os


logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(message)s')
logger = logging.getLogger()


def go(args):

    # run = wandb.init(job_type='basic_cleaning')
    run = wandb.init(project = 'nyc_airbnb', group = 'eda', save_code = True, job_type = 'basic_cleaning')
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################
    logger.info('Downloading artifact')
    local_path = wandb.use_artifact(args.input_artifact).file()
    df = pd.read_csv(local_path)

    logger.info('Setting a reasonable range for price')
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()

    logger.info('Converting date variables from string to datetime')
    df['last_review'] = pd.to_datetime(df['last_review'])

    df.info()
    
    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()

    df.to_csv('clean_sample.csv', index = False)

    artifact = wandb.Artifact(args.output_artifact, type = args.output_type, description = args.output_description)
    artifact.add_file('clean_sample.csv')
    
    logger.info('Logging artifact')
    run.log_artifact(artifact)

    os.remove('clean_sample.csv')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='A very basic data cleaning')


    parser.add_argument(
        '--input_artifact', 
        type = str, ## INSERT TYPE HERE: str, float or int
        help = 'Name of the input artifact', ## INSERT DESCRIPTION HERE
        required = True
    )

    parser.add_argument(
        '--output_artifact', 
        type = str, ## INSERT TYPE HERE: str, float or int
        help = 'Name of the output artifact', ## INSERT DESCRIPTION HERE
        required = True
    )

    parser.add_argument(
        '--output_type', 
        type = str, ## INSERT TYPE HERE: str, float or int
        help = 'Type of the output artifact', ## INSERT DESCRIPTION HERE
        required = True
    )

    parser.add_argument(
        '--output_description', 
        type = str, ## INSERT TYPE HERE: str, float or int
        help = 'Description for the output artifact', ## INSERT DESCRIPTION HERE
        required = True
    )

    parser.add_argument(
        '--min_price', 
        type = float, ## INSERT TYPE HERE: str, float or int
        help = 'A reasonable minimum price', ## INSERT DESCRIPTION HERE
        required = True
    )

    parser.add_argument(
        '--max_price', 
        type = float, ## INSERT TYPE HERE: str, float or int
        help = 'A reasonable maximum price', ## INSERT DESCRIPTION HERE,
        required = True
    )


    args = parser.parse_args()

    go(args)
