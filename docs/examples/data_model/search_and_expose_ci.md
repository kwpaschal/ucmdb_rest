# Searching for CIs in UCMDB

This example demonstrates how to search for Configuration Items (CIs) in your UCMDB server using the `data_model` module.

!!! info "Environment Awareness"
    The library automatically detects the UCMDB server version upon connection. 
    You can access this via **`client.server_version`**, which returns a tuple (e.g., `(11, 6, 0)`). This is useful for conditional logic if certain API features require a specific UCMDB version.

## Python Example

```python
--8<-- "examples/search_and_expose_ci.py"
```

# Key Parameters

When using `search_by_label`, you must specify some parameters:

* **pattern**: 
    * Type: `String`
    * Description: This is a pattern or exact name you are looking for.  To specify a pattern
    that will match all CIs that start with "aws" you could use:  "aws%".  To specify a pattern
    that will match all CIs that have "aws" in them, you could use: "%aws%".  Likewise you can 
    specify "aws" for specifically one node that matches "aws" as its complete display label.
* **CI Type**: 
    * Type: `String` 
    * Description: This parameter will specify what CI type and children you are trying to find.
    Node, for example, includes node, windows (nt), unix, etc.
* **layout**: 
    * Type: `List of Strings`
    * Description: You can specify which attribute you want to return.