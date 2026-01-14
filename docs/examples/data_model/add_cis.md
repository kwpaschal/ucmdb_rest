# Adding CIs to UCMDB

This example demonstrates how to add new Configuration Items (CIs) and relationships to your UCMDB server using the `data_model` module.

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