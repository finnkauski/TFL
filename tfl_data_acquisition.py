# %%

# Scroll closer to the bottome, there you'll find the download media function
# call please change that to where you want your videos and images saved to.

# TO DO:
#  1. Implement Memoisation for image downloading. No point accidentally
#     reruning stuff.

import time
import os
import requests as r
import json
import pandas as pd
import urllib
from dask.distributed import Client
from dask import delayed


class CamSession():

    url = "https://api.tfl.gov.uk/Place/Type/JamCam"

    def __init__(self):
        ''' Initialise class and read the JSON respons from the API '''

        self.raw_json = r.get(self.url).json()
        self.client = Client()


    def parse(self, cols=["imageUrl", "videoUrl"]):
        ''' Parse the response from the API

            cols - list of columns to extract datetimes from


        '''

        self.parsed_json = {

            di["commonName"]: di for di in self.raw_json

        }

        for key in self.parsed_json:

            di = self.parsed_json[key]

            result = {}

            # Pick out the relevant Long and Lat values, might need them

            result["lat"] = di["lat"]

            result["lon"] = di["lon"]

            # Use list comprehension to pick up the other key stuff

            result.update(

                {

                    di2["key"]:

                    di2["value"] if di2["key"] not in cols


                    else [di2["value"], di2["modified"]]


                    for di2 in di["additionalProperties"]

                }


            )

            self.parsed_json[key] = result

        # Parse the dictionary into a dataframe

        self.parsed_df = pd.DataFrame(self.parsed_json).T

        # for the preset columns that we collected the time modified, split it
        # out into two seperate columns

        for col in cols:

            self.parsed_df[[col, col + "_time"]] = pd.DataFrame(

                self.parsed_df[col].tolist(),
                index=self.parsed_df.index

            )

    def download_media(self, url_col, path):
        '''

        Function to download images from the API responses
        At the moment this doesn't involve multithreading.

        Takes about 4 min 30 secs to complete

        Not happy about specifying path as a string, should use pathlib
        or at least os.joins >:( need more time to iron this out laters.

        '''
        self.path = path

        with mt.ThreadPoolExecutor(16) as pool:

            pool.map(self.fetch, df["imageUrl"])

        print(" -- Downloading")

    def fetch(self, url, path=self.path):

        for url in self.parsed_df[url_col].values:

            file_name = urllib.parse.urlsplit(url).path.split(sep="/")[-1]

            urllib.request.urlretrieve(url, path + "/" + file_name)

        time.sleep(1)


if __name__ == "__main__":

    obj = CamSession()
    obj.parse()
    obj.download_media("imageUrl", r"/Users/arturas/projects/tfl/images")
#    obj.download_media("videoUrl", "/home/finn/Desktop/Link to TFL/videos")
    result = obj.raw_json
    df = obj.parsed_df
