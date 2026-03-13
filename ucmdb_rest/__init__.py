from importlib.metadata import PackageNotFoundError, version

from .client import UCMDBAuthError, UCMDBServer

# Only keep utilities that are strictly helper functions 
# and don't require an active server connection to exist.
__all__ = ['UCMDBServer', 'UCMDBAuthError']
try:
    __version__ = version("ucmdb_rest")
except PackageNotFoundError:
    __version__ = "unknown"