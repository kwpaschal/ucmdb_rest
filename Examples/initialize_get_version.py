import ucmdb_rest

myServer = ucmdb_rest.UCMDBServer("admin",
                                  "adminPassword",
                                  "myucmdb.mycompany.com",
                                  8443,
                                  "https",
                                  False,
                                  1,
                                  True)
version = myServer.system.getUCMDBVersion()
version_data = version.json()
print(f'Product: {version_data["productName"]}')
print(f'Server Version: {version_data["fullServerVersion"]}')
print(f'Content Pack: {version_data["contentPackVersion"]}')
print(f'Server Build: {version_data["serverBuildNumber"]}')
print(f'My server version from the client: {myServer.version}')
print(version_data)