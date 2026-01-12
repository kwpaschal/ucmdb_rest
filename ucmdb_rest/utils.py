from functools import wraps


def requires_version(min_version_tuple):
    """
    Decorator to gate methods based on the UCMDB server version.

    This decorator compares the server version stored in the client instance 
    against a required minimum. It is designed to be used on methods within 
    service classes (e.g., Topology, System) that have a 'self.client' attribute.

    Parameters
    ----------
    min_version_tuple : tuple of int
        The minimum version required to execute the method (e.g., (11, 13, 0)).

    Raises
    ------
    RuntimeError
        If the connected UCMDB server version is lower than the required 
        minimum version.

    Notes
    -----
    All methods present in the library as of UCMDB 2023.05 (internal version 11.6.11) 
    are considered the baseline and do not require this decorator. Use this 
    for any functionality added in later releases.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # 'self' here refers to the service instance (e.g., Topology)
            # 'self.client.version' is the tuple we stored in UCMDBServer
            if self.client.version < min_version_tuple:
                current_v = ".".join(map(str, self.client.version))
                req_v = ".".join(map(str, min_version_tuple))
                raise RuntimeError(
                    f"Method '{func.__name__}' requires UCMDB {req_v} or newer. "
                    f"Current server version is {current_v}."
                )
            return func(self, *args, **kwargs)
        return wrapper
    return decorator