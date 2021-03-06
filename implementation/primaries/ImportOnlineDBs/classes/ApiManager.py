from implementation.primaries.ImportOnlineDBs.classes import MScoreApi
import os
from implementation.primaries import exceptions


class ApiManager(object):

    def __init__(self, folder="", logger=None):
        self.logger = logger
        self.folder = folder
        self.sources = {}
        try:
            MScoreApi.MuseScoreApi.getKey(MScoreApi.MuseScoreApi.env_key)
            self.sources["MuseScore"] = (
                MScoreApi.MuseScoreApi(folder), [
                    "movement-title", "work-title", "creator"])
        except exceptions.APIKeyNotFoundException:
            if self.logger is not None:
                self.logger.exception(
                    "MuseScore API key not found. MSCORE Api disabled.")

    def fetchAllData(self):
        '''
        method to get data from every source and merge it into 1 dictionary
        :return: dictionary indexed by source name
        '''
        results = {}
        for source_id in self.sources:
            result_set = self.sources[source_id][0].cleanCollection()
            results[source_id] = {
                result["id"]: result for result in result_set}
        return results

    def downloadAllFiles(self, extension="mxl"):
        '''
        method to take the data from fetchAll and from that collect the files
        :return: dictionary indexed by source name. each key links to a list of file locations where the new XML files are stored.
        '''
        results = {}
        data_set = self.fetchAllData()
        return self.downloadFiles(data_set, extension=extension)

    def downloadFiles(self, dataset, extension="mxl"):
        '''
        method to take the data from fetchAll and from that collect the files
        :return: dictionary indexed by source name. each key links to a list of file locations where the new XML files are stored.
        '''
        results = {}
        for source_id in dataset:
            data_list = []
            for file in dataset[source_id]:
                id = file
                secret = dataset[source_id][id]["secret"]
                status = self.sources[source_id][
                    0].downloadFile(id, secret, type=extension)
                if(status == 200):
                    location = os.path.join(id + "." + extension)
                    data_list.append(location)
            results[source_id] = data_list
        return results

    def downloadFile(
            self,
            source="MuseScore",
            file="",
            secret="",
            extension="mxl"):
        '''
        method to fetch 1 single file from a selected source
        :param source: the api source where it's located
        :param file: the file id or name it is known as
        :param secret: the password or secret to access it
        :return: status code of request
        '''
        status = 0
        if source in self.sources:
            status = self.sources[source][0].downloadFile(
                file, secret, type=extension)
        else:
            status = 4004
        return status

    def getSourceIgnoreList(self, source):
        if source in self.sources:
            return self.sources[source][1]
