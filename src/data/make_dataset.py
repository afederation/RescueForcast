# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_doten

def load_raw_sar_data(input_filepath):
    sar_header = ['DEM', 'date', 'name', 'responders', 'hours', 'miles']
    sar_data = pd.read_csv(f'{input_filepath}KCSARA.csv', header=None,
                           parse_dates=['date'], names=sar_header)
    sar_data = pd.DataFrame(sar_data)
    sar_data.header = sar_header

    return sar_data

def clean_sar_data(df, date_range):
    '''
    Create a df that contains all dates within the
    date range and returns whether a call happened
    on that day or not.
    '''
    clean_table = []

    for d in date_range:
        if sar_data.date.isin([d]).any():
            clean_table.append([d,1])
        else:
            clean_table.append([d,0])
    sar_clean = pd.DataFrame(clean_table)
    sar_clean.columns = ['date','mission']

    add_datepart(sar_clean, 'date', drop=False)

    return sar_clean

@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    # SAR call data pre-processing
    df = load_raw_sar_data(input_filepath)
    date_range = pd.date_range(start='1/1/2002', end='4/01/2019')
    df = clean_sar_data(df, date_range)

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
