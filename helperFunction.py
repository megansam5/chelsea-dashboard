import csv
import os
from  requests import get
from time import sleep

def removeCSV(object, writePath):
    file_prefix1 = object

    # Delete all CSV files with same prefix and ending in CSV
    try:
        for file in os.listdir(writePath):
            if file.strip().startswith(file_prefix1) and file.upper().endswith('.CSV'):
                os.remove(os.path.join(writePath, file))
                print("file deleted", file)
    except Exception as error:
        print(error)
        raise

def writeData2CSV(file_name, writePath, col_names, row_data):

    op_file = os.path.join(writePath, file_name)

    try:
        with open(op_file, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=col_names, quoting=csv.QUOTE_MINIMAL)

            writer.writeheader()
            for row in row_data:
                writer.writerow(row)
        print('Data written to {}'.format(op_file))
    except Exception as error:
        print(error)
        raise



def wrappedRequest( url, params, headers,proxies=None, retry=3 ):

    lastException = None
    interval = 5.0
    x = 0
    for x in range(retry):
        try:
            print(url, params, proxies, headers)

            result = get(url, params, proxies= proxies, headers=headers)

            if result is not None and result.status_code != 200 and (x + 1) < retry:
                print(
                    'Encountered response code {e}, sleeping for {i} seconds'.format(e=result.status_code, i=interval * (x + 1)))
                sleep(interval * (x + 1))
                continue
            return {"result":result, "retry":x}
        except Exception as e:
            lastException = e
            if (x+1) < retry:
                print('Encountered exception {e}, sleeping for {i} seconds'.format(e=lastException, i=interval * (x+1)))
                sleep(interval*(x+1))


    if lastException is not None:
        raise
