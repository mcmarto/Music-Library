'''
Classes dealing with the MuseScore community api
'''
from implementation.primaries.ImportOnlineDBs.classes.API import Api

from implementation.primaries.GUI.helpers import get_base_dir
import requests
import os
import shutil
import gzip
from io import BytesIO
from implementation.primaries import exceptions
import logging
import json


class MuseScoreApi(Api):
    env_key = 'MSCORE'

    def __init__(self, folder="", logger=None):
        Api.__init__(self, folder=folder)
        self.logger = logger
        self.key = self.getKey(self.env_key)
        self.params = {'oauth_consumer_key': self.key}
        self.endpoint = 'http://api.musescore.com/services/rest/score.json'
        self.download_endpoint = 'http://static.musescore.com/'
        self.ignored_tags = ["movement-title", "work-title", "creator"]

    def getCollection(self):
        '''
        method which pulls all data from the api
        :return: list of dictionaries containing metadata about all pieces licensed to modify commercially
        '''
        request = requests.get(self.endpoint, params=self.params)
        if request.status_code == 200:
            response = request.json()
        else:
            self.logger.exception(
                "API request response code: {} in getCollection".format(
                    request.status_code))
            raise exceptions
        return response

    def cleanCollection(self):
        '''
        method which pulls data and extracts only what we need. Note that whilst key signature is part of the API,
        this is not considered useful as it only provides the first key signature of the piece.
        :return: list of dictionaries containing data useful to the application
        '''
        collection = self.getCollection()
        results = []
        for element in collection:
            data = {}
            data["id"] = element["id"]
            data["secret"] = element["secret"]
            data["title"] = element["metadata"]["title"]
            data["composer"] = element["metadata"]["composer"]
            data["lyricist"] = element["metadata"]["poet"]
            data["license"] = element["license"]
            results.append(data)
        return results

    def downloadFile(self, fname, secret, type='mxl'):
        '''
        method to download a file
        :param fname: ID of the file
        :param secret: code to get the file
        :param type: the file extension to download
        :return: status code of request
        '''
        endpoint = self.download_endpoint + \
            str(fname) + "/" + str(secret) + "/score." + type
        request = requests.get(endpoint, stream=True)
        if request.status_code == 200:
            with open(os.path.join(self.folder, str(fname) + "." + type), 'wb') as f:
                request.raw.decode_content = True
                shutil.copyfileobj(request.raw, f)
        return request.status_code

    def searchForExactMatch(self, filters):
        '''
        method to search the db for specific things. This will apply each filter in turn,
        and then extract the results which exist in every response.
        :param filters: a dictionary of things to filter it by. The value of each entry should be a list.
        :return: list of exact matches
        '''
        collection = []
        data = {}
        for filter in filters:
            params = self.params
            for value in filters[filter]:
                params.update({filter: value})
                request = requests.get(self.endpoint, params=params)

                if request.encoding == 'gzip':
                    buf = StringIO(request.content)
                    f = gzip.GzipFile(fileobj=buf)
                    response = json.load(f.read())
                else:
                    response = request.json()
                if request.status_code == 204:
                    logging.log(logging.ERROR, "No JSON content")

                current_response = {r["id"]: r for r in response}
                data.update(current_response)
                response_ids = [r["id"] for r in response]
                collection.append(set(response_ids))
        collection_set = set.intersection(*collection)
        collection_list = [data[key] for key in collection_set]
        return collection_list

    def search(self, filters):
        '''
        method to search the api for all given filters.
        :param filters: dictionary of filters. Each value should be a list
        :return: dictionary of responses, indexed by the value each response used to get the data.
        '''
        collection = {}
        for filter in filters:
            params = self.params
            for value in filters[filter]:
                params.update({filter: value})
                request = requests.get(self.endpoint, params=params)
                response = request.json()
                collection[value] = response

        return collection
