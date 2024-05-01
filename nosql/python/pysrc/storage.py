""" module storage.py, Chris Joakim, Microsoft, 2023 """

import traceback

from azure.storage.blob import BlobServiceClient

class Storage():
    """
    This class is used to access an Azure Storage account.
    """
    def __init__(self, opts):
        acct_name = opts['acct']
        acct_key  = opts['key']
        acct_url  = f'https://{acct_name}.blob.core.windows.net/'
        self.blob_service_client = BlobServiceClient(
            account_url=acct_url, credential=acct_key)

    def account_info(self):
        """ Return the account information. """
        return self.blob_service_client.get_account_information()

    def list_containers(self):
        """ Return the list of container names in the account. """
        clist = []
        try:
            containers = self.blob_service_client.list_containers(include_metadata=True)
            for container in containers:
                clist.append(container)
            return clist
        except Exception as excp:
            print(str(excp))
            print(traceback.format_exc())
            return None

    def create_container(self, cname):
        """ Create a container in the account. """
        try:
            container_client = self.blob_service_client.get_container_client(cname)
            container_client.create_container()
        except Exception as excp:
            print(str(excp))
            print(traceback.format_exc())

    def delete_container(self, cname):
        """ Delete a container in the account. """
        try:
            container_client = self.blob_service_client.get_container_client(cname)
            container_client.delete_container()
        except Exception as excp:
            print(str(excp))
            print(traceback.format_exc())

    def list_container(self, cname):
        """ Return the list of blobs in the container. """
        try:
            container_client = self.blob_service_client.get_container_client(cname)
            return container_client.list_blobs()
        except Exception as excp:
            print(str(excp))
            print(traceback.format_exc())
            return None

    def upload_blob_from_file(self, local_file_path, cname, blob_name, overwrite=True):
        """ Upload a blob from a local file. """
        try:
            blob_client = self.blob_service_client.get_blob_client(container=cname, blob=blob_name)
            with open(local_file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=overwrite)
            return True
        except Exception as excp:
            print(str(excp))
            print(traceback.format_exc())
            return False

    def upload_blob_from_string(self, string_data, cname, blob_name, overwrite=True):
        """ Upload a blob from a string. """
        try:
            blob_client = self.blob_service_client.get_blob_client(container=cname, blob=blob_name)
            blob_client.upload_blob(string_data, overwrite=overwrite)
            return True
        except Exception as excp:
            print(str(excp))
            print(traceback.format_exc())
            return False

    def download_blob(self, cname, blob_name, local_file_path):
        """ Download a blob to a local file. """
        try:
            blob_client = self.blob_service_client.get_blob_client(container=cname, blob=blob_name)
            with open(local_file_path, "wb") as download_file:
                download_file.write(blob_client.download_blob().readall())
        except Exception as excp:
            print(str(excp))
            print(traceback.format_exc())

    def download_blob_to_string(self, cname: str, blob_name: str) -> str:
        """ Download a blob to a string. """
        blob_client = self.blob_service_client.get_blob_client(container=cname, blob=blob_name)
        downloader = blob_client.download_blob(max_concurrency=1, encoding='UTF-8')
        return downloader.readall()
