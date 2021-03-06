#!/usr/bin/python
#
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This example illustrates how to update a report."""

import argparse
import sys

import dfareporting_utils
from oauth2client import client

# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument(
    'profile_id', type=int,
    help='The ID of the profile to update a report for')
argparser.add_argument(
    'report_id', type=int,
    help='The ID of the report to update')


def main(argv):
  # Retrieve command line arguments.
  flags = dfareporting_utils.get_arguments(argv, __doc__, parents=[argparser])

  # Authenticate and construct service.
  service = dfareporting_utils.setup(flags)

  profile_id = flags.profile_id
  report_id = flags.report_id

  try:
    # Construct a get request for the specified report.
    request = service.reports().get(profileId=profile_id, reportId=report_id)

    # Execute request
    response = request.execute()

    # Create a report resource with the fields to update
    report = {
        'accountId': response['accountId'],
        'id': response['id'],
        'lastModifiedTime': response['lastModifiedTime'],
        'name': 'Example Standard Report (Updated)',
        'ownerProfileId': response['ownerProfileId'],
        'type': response['type']
    }

    # Create the update request
    request = service.reports().update(
        profileId=profile_id, reportId=report_id, body=report)

    # Execute request and print response.
    result = request.execute()

    print ('Successfully updated %s report with id "%s".'
           % (result['type'], result['id']))

  except client.AccessTokenRefreshError:
    print ('The credentials have been revoked or expired, please re-run the '
           'application to re-authorize')


if __name__ == '__main__':
  main(sys.argv)
