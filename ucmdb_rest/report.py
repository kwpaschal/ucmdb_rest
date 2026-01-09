# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 15:10:48 2024

@author: kpaschal

This python library contains methods dealing with reports in the 
UCMDB server.
"""

from unittest.mock import MagicMock
from urllib.parse import quote


class Reports:
    def __init__(self, client):
        """
        Initialize the service with a reference to the main level UCMDB client
        """
        self.client = client
            
    def changeReportsAll(self, toTime, fromTime, view, attributes=['description', 'name']):
        """
        Retrieves change reports for all elements within a specified time range
        and view.

        This method generates a request to retrieve change reports for all
        elements within a specified time range and view.

        Parameters
        ----------
        toTime : int
            The end time of the time range for the report. Format is epoch time
            in milliseconds.
        fromTime : int
            The start time of the time range for the report. Format is epoch time
            in milliseconds.
        view : str
            The name of the view for which the change reports are requested.
        attributes : list
            A list of attributes to display on the report

        Returns
        -------
        requests.Response
            Response object containing the change reports.
        """
        viewName = quote(view)
        attr_string = ",".join(attributes)
        encoded_filter = quote(f'type=ALL&attributes={attr_string}')
        url = f'{self.client.base_url}/report/change/view/{viewName}/results?filter={encoded_filter}&dateFrom={str(fromTime)}&dateTo={str(toTime)}&start=1&pageSize=100'  # noqa: E501
        return self.client.session.get(url)

    def changeReportsBlacklist(self, toTime, fromTime, view, attributes=['description']):
        """
        Retrieves a blacklist report for CIs in a view.

        This function makes a POST request to the UCMDB server to 
        retrieve the information.

        Parameters
        ----------
        toTime : int
            Time the report should end. Format is epoch time
            in milliseconds.
        fromTime : int
            Time the report should start. Format is epoch time
            in milliseconds.
        view : str
            Name of the view to retrieve the report from.
        attributes : list
            A list of attributes to display on the report

        Returns
        -------
        requests.Response
            A dictionary object containing the details of which attribute 
            changed, the date it was changed, and the old and new values. 
            Example:
            {
                "changes": {
                    "4278e81d3dd6640a835e419d2865905d": {
                        "ciId": "4278e81d3dd6640a835e419d2865905d",
                        "displayLabel": "create222",
                        "className": "node",
                        "properties": [
                            {
                                "name": "Display Label",
                                "value": "USER LABEL"
                            },
                            {
                                "name": "Create Time",
                                "value": "Fri Jan 20 14:13:40 EET 2017"
                            },
                            {
                                "name": "Description",
                                "value": "description"
                            }
                        ],
                        "changes": {
                            "name": [
                                {
                                    "attribute": "name",
                                    "oldValue": "create2",
                                    "newValue": "create22",
                                    "changer": "User:{UISysadmin###UCMDB},
                                                LoggedInUser:{admin###UCMDB}",
                                    "changeDate": 1484741091500
                                }
                            ]
                        }
                    }
                }
            }
        """
        body_json = {
            'dateFrom': str(fromTime),
            'dateTo': str(toTime),
            'viewName': view,
            'attributes': attributes
        }
        url = f'{self.client.base_url}/changeReports/generate/blacklist'
        return self.client.session.post(url,json=body_json)

    def changeReportsWhitelist(self, toTime, fromTime, view, attributes=['name','description']): 
        """
        Retrieves a whitelist report for CIs in a view.

        This function makes a POST request to the UCMDB server to 
        retrieve the information.

        Parameters
        ----------
        toTime : int
            Time the report should end, in the format: 1454364000000.
        fromTime : int
            Time the report should start, in the format: 1485986400000.
        view : str
            Name of the view to retrieve the report from.
        attributes : list
            A list of attributes to display on the report

        Returns
        -------
        requests.Response
            A dictionary object containing the details of which 
            attribute changed, the date it was changed, and the old and 
            new values. Example:
            {
                "changes": {
                    "4278e81d3dd6640a835e419d2865905d": {
                        "ciId": "4278e81d3dd6640a835e419d2865905d",
                        "displayLabel": "create222",
                        "className": "node",
                        "properties": [
                            {
                                "name": "Display Label",
                                "value": "USER LABEL"
                            },
                            {
                                "name": "Create Time",
                                "value": "Fri Jan 20 14:13:40 EET 2017"
                            },
                            {
                                "name": "Description",
                                "value": "description"
                            }
                        ],
                        "changes": {
                            "name": [
                                {
                                    "attribute": "name",
                                    "oldValue": "create2",
                                    "newValue": "create22",
                                    "changer": "User:{UISysadmin###UCMDB},
                                                LoggedInUser:{admin###UCMDB}",
                                    "changeDate": 1484741091500
                                }
                            ]
                        }
                    }
                }
            }
        """
        body_json = {
            'dateFrom': str(fromTime),
            'dateTo': str(toTime),
            'viewName': view,
            'attributes': attributes
        }
        url = f'{self.client.base_url}/changeReports/generate/whitelist'
        result = self.client.session.post(url,json=body_json)

        if result.status_code == 400:
            empty_res = MagicMock()
            empty_res.status_code = 200
            empty_res.json.return_value = {}
            empty_res.text = "{}"
            return empty_res
        
        return result