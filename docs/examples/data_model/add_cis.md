# Adding CIs to UCMDB

This example demonstrates how to add new Configuration Items (CIs) and relationships to your UCMDB server using the `data_model` module.

!!! info "Environment Awareness"
    The library automatically detects the UCMDB server version upon connection. 
    You can access this via **`client.server_version`**, which returns a tuple (e.g., `(11, 6, 0)`). This is useful for conditional logic if certain API features require a specific UCMDB version.

## Python Example

```python
--8<-- "examples/add_cis.py"
```

# Key Parameters

When using `add_cis`, you can specify optional flags:

* **global_ids**: 
    * Type: `Boolean`
    * Description: Returns the global ID instead of the local UCMDB ID.
* **force_temp**: 
    * Type: `Boolean` 
    * Description: Use this if you want to bypass standard identification and force a temporary CI.
* **ignore_existing**: 
    * Type: `Boolean`
    * Description: If the CI is already there, don't throw an error, just skip it.