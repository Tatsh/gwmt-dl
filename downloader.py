#!/usr/bin/python
#
# Copyright 2011 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Module for downloading CSV files from Google Webmaster Tools.

Module handles authentication with the Google servers by using the gdata
module provided by Google.  This script requires the gdata package be
installed in order to run.

  Downloader: Handles download implementation.
"""


import json
import gdata.webmastertools.service


class Downloader(object):
  """Handles client authentication and requests for Webmaster data.

  Contains the logic needed to authenticate with Google servers and
  download CSV files from Webmaster Tools.
  """
  HOST = 'www.google.com'
  APP_NAME = 'Google-WMTdownloadscript-0.1'
  LIST_PATH = '/webmasters/tools/downloads-list?hl=%s&siteUrl=%s'
  FILE_NAME_HEADER = 'content-disposition'
  TEXT_BEFORE_NAME = 'attachment; filename='

  def __init__(self):
    self._client = gdata.webmastertools.service.GWebmasterToolsService()
    self._logged_in = False
    self._language = 'en'
    self._downloaded = []

  def IsLoggedIn(self):
    """Check if client has logged into their Google account yet."""
    return self._logged_in

  def LogIn(self, email, password, captcha_answer=None):
    """Attempts to log into the specified Google account.

    Args:
      email: User's Google email address.
      password: Password for Google account.
      captcha_answer: Optional answer to the captcha challenge.

    Raises:
      CaptchaRequired: If the login service requires a captcha response.
      BadAuthentication: If email/password is incorrect.
    """
    if self._client.captcha_token and captcha_answer:
      self._client.ClientLogin(email, password, source=self.APP_NAME,
                               captcha_token=self._client.captcha_token,
                               captcha_response=captcha_answer)
    else:
      self._client.ClientLogin(email, password, source=self.APP_NAME)

    self._logged_in = True

  def DoDownload(self, site, tables_to_download):
    """Download CSV files and write them to disk.

    Downloader must be logged in before this method can be called, otherwise
    it will raise a ValueError.

    Args:
      site: URL for a website managed by the webmaster.
      tables_to_download: List of features that should be downloaded.

    Raises:
      ValueError: If the client has not logged in yet.
    """
    if not self.IsLoggedIn():
      raise ValueError('Client not logged in.')

    available = self._GetDownloadList(site)
    sites_json = json.loads(available)

    for key in tables_to_download:
      url = sites_json.get(key)
      if url:
        self._DownloadFile(url)

  def GetDownloadedFiles(self):
    """Get a list of downloads that have been written to disk.

    Returns:
      A list containing the names of all the downloaded files that have been
      written by this module.
    """
    return self._downloaded

  def GetCaptchaUrl(self):
    return self._client.captcha_url

  def SetLanguage(self, language_code):
    self._language = language_code

  def _GetDownloadList(self, site):
    """Query the server for list of download URLs.

    Args:
      site: URL for a website managed by the webmaster.

    Returns:
      A string of JSON data giving a mapping between Webmaster Tools features
      and download URLs.  For example:

      {'TOP_QUERIES':'webmaster/tools/top-search-queries-dl?...'}
    """
    url = self._GetFullUrl(self.LIST_PATH % (self._language, site))
    res_stream = self._client.request('GET', url)
    download_list = res_stream.read()
    res_stream.close()
    return download_list

  def _GetFullUrl(self, path):
    """Construct an absolute URL using path segment.

    Args:
      path: The path segment of a URL.

    Returns:
      A URL giving the absolute path to a resource.
    """
    return 'https://' + self.HOST + path

  def _DownloadFile(self, path):
    """Download the file and write it to disk.

    Downloads the file based on the given URL.  The file name of the download
    is included in the header.  Prints the file name to standard out.

    Args:
      path: The path segment of the URL to download.
    """
    url = self._GetFullUrl(path)
    in_stream = self._client.request('GET', url)
    file_name = in_stream.getheader(self.FILE_NAME_HEADER)
    file_name = file_name.lstrip(self.TEXT_BEFORE_NAME)
    self._downloaded.append(file_name)
    out_file = open(file_name, 'w')
    out_file.write(in_stream.read())

    in_stream.close()
    out_file.close()
