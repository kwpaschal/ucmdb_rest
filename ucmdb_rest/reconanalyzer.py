"""
Created on Wed Jun  5 16:19:14 2024

@author: kpaschal

This library contains methods to work with the reconciliation analyzer.
"""

import requests

from .utils import _url
from . import config

def reconAnalyzerByName(token, udserver, ci):
    """
    This method generates a GET method to the UCMDB REST API to get a CI
    from the reconciliation analyzer.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass,
        and ucmdb_server.
    udserver : str
        UCMDB server hostname or IP address.
    ci : str
        Name of the host to look up in the reconciliation analyzer.

    Returns
    -------
    requests.Response
        Returns a list of dictionaries. Each one containing the cmdb id,
        name and type of entry. For example:

            [
                {
                    "cmdb_id": "4c5c605b7af89deab868c04bebceed3a",
                    "name": "node1",
                    "type": null
                },
                {
                    "cmdb_id": "4f4a843d6e4c6977b48d573b21adc5ed",
                    "name": "node1",
                    "type": null
                },
                {
                    "cmdb_id": "45379ecec194c3318489f641c4b8ab32",
                    "name": "node1",
                    "type": null
                },
                {
                    "cmdb_id": "4c96f4b6d0bef110b3ac13d686a7b2cd",
                    "name": "node1",
                    "type": null
                },
                {
                    "cmdb_id": "4e235cf3cb1b100a863eb7101d4fdced",
                    "name": "node1",
                    "type": null
                }
            ]

    """
    return requests.get(
        _url(udserver, '/v1/recon-analyzer/ci?name=' + ci), 
        headers=token, 
        verify=config.get_verify_ssl()
    )

def reconAnalyzerOperationByID(token, udserver, ci_id):
    """
    This method does a GET call to the UCMDB REST API. It retrieves the
    operation for a given UCMDB ID.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass,
        and ucmdb_server.
    udserver : str
        UCMDB server hostname or IP address.
    ci_id : str
        UCMDB ID of the CI to look up in the reconciliation analyzer.

    Returns
    -------
    requests.Response
        A list of dictionaries, each dictionary listing what kind of
        operation was performed on the CI. For example:

            [
                {
                    "timestamp" : 1718402068123,
                    "id" : "2103768088",
                    "operationType" : "addOrUpdate",
                    "errorMessage" : null,
                    "customerId" : "1",
                    "changer" : "FTC06UCM43",
                    "dataToUpdateSize" : 1,
                    "referenceDataSize" : 0,
                    "identificationDuration" : 34,
                    "dataInAnalysisDuration" : 2,
                    "maxTopologyLevel" : 1,
                    "numberOfMergedCIs" : 0,
                    "numberOfTypeChanges" : 0,
                    "numberOfMergeOperations" : 0,
                    "numberOfIgnoresFromCmdb" : 0,
                    "numberOfIgnoresInBulk" : 0,
                    "numberOfObjectsToUpdateByType" : {
                        "node" : 1
                    },
                    "statistics" : { },
                    "properties" : {
                        "lic_operational2advanced" : false,
                        "lic_type_asset" : false,
                        "lic_type_management" : false,
                        "global_id" : "4e235cf3cb1b100a863eb7101d4fdced",
                        "cmdb_id" : "4e235cf3cb1b100a863eb7101d4fdced",
                        "serial_number" : "54321.0",
                        "type" : "node",
                        "last_discovered_by_probe" : "FTC06UCM43",
                        "data_source" : "ZONE_[INTEGRATION]_JOB_DS_inpt2",
                        "root_iscandidatefordeletion" : false,
                        "display_label" : "node1",
                        "lic_type_premium" : false,
                        "host_iscomplete" : false,
                        "name" : "node1",
                        "default_gateway_ip_address_type" : "IPv4",
                        "bios_uuid" : "123ABC"
                    },
                    "changedAttributes" : [ ]
                }
            ]

    """
    return requests.get(
        _url(udserver, '/v1/recon-analyzer/operation/ci/' + ci_id), 
        headers=token, 
        verify=config.get_verify_ssl()
    )

def reconAnalyzerMatchReason(token, udserver, opid, ciid):
    """
    This method generates a GET call to the UCMDB REST API to get the
    match reason for a given operation ID and CI ID.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass,
        and ucmdb_server.
    udserver : str
        UCMDB server hostname or IP address.
    opid : str
        UCMDB Operation ID which generated some change.
    ciid : str
        UCMDB CI ID on which the operation ran.

    Returns
    -------
    requests.Response
        Shows identification and matches (empty if none). For example:

            {
                "identifications": [],
                "matches": []
            }

    """
    return requests.get(
        _url(udserver, 
             '/v1/recon-analyzer/reconDetails/' + str(opid) + '/' + str(ciid)
        ), 
        headers=token, 
        verify=config.get_verify_ssl()
    )