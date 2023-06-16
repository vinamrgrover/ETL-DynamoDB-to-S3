import pandas as pd
import requests
import os
import json
import re
from decimal import Decimal
import boto3
from datetime import datetime

def get_data(api_key) -> str:
    url = f'https://my.api.mockaroo.com/users.json?key={api_key}'
    response = requests.get(url)
    return response.json()


def cast_val(val: str, dtype: type):
    try:
        return dtype(val)
    except TypeError:
        return None
    except ValueError:
        return None


def filter_df(df: pd.DataFrame) -> pd.DataFrame:
    df.price = df.price.map(lambda p: cast_val(
        re.search(r'\d+\\[.]\d+', p) \
            .group() \
            .replace('\\', '')
        , float))

    df.color = df.color.fillna('undefined')

    df.quantity = df.quantity.fillna(0) \
        .apply(lambda q: cast_val(q, int)) \
        .replace(0, None)

    df.insert(5, 'country', value=df.location.apply(lambda l: re.match(r'[A-Z a-z]+', l).group().strip()))

    df.insert(6, 'city', value=df.location.apply(lambda l: re.search(r'-[A-Z a-z]+', l) \
                                                 .group() \
                                                 .replace('- ', '') \
                                                 .strip()))

    df.price = df.price.apply(lambda p: Decimal(str(p)))  # DynamoDB doesn't support float

    df.drop(['location'], axis=1, inplace=True)
    
    df = df.assign(created_at = lambda _ : datetime.strftime(datetime.now(), '%Y-%m-%d %H'))

    return df


def dynamodb_write(df: pd.DataFrame) -> str:
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Flowers')

    with table.batch_writer() as batch:
        for index, row in df.iterrows():
            item = row.to_dict()
            batch.put_item(Item=item)

    return f'{len(df)}'


def lambda_handler(event=None, context=None) -> dict:
    df = pd.read_json(
        json.dumps(
            get_data(os.getenv('api_key'))
        )
    )

    df = filter_df(df)
    row_count = dynamodb_write(df)

    glue = boto3.client('glue', region_name = 'ap-south-1')
    
    response = glue.start_job_run(
        JobName = 'DynamoDB_to_S3'
        )
        
    return {
        'StatusCode': 200,
        'RowsWritten': row_count,
        'JobRunId' : response['JobRunId']
    }

