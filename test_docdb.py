import pymongo
import sys
import paramiko
import sshtunnel

from Config import Config

aws_config = Config.get_instance()['AWS']
db_host = aws_config['DOCDB_HOST']
db_port = aws_config['DOCDB_PORT']
db_user = aws_config['DOCDB_USER']
db_pass = aws_config['DOCDB_PASS']

private_key = paramiko.RSAKey.from_private_key_file(f"./{aws_config['EC2_KEY']}")

# https://stackoverflow.com/questions/58373690/connecting-to-mysql-database-via-ssh-over-a-jump-host-using-python-3
# https://stackoverflow.com/questions/45213676/access-remote-db-via-ssh-tunnel-python-3
with sshtunnel.SSHTunnelForwarder(
        (aws_config['EC2_HOST'], int(aws_config['EC2_PORT'])),
        ssh_username=aws_config['EC2_USER'],
        ssh_pkey=private_key,
        remote_bind_address=(db_host, int(db_port))
) as tunnel:
    port = tunnel.local_bind_port

    # Create a MongoDB client, open a connection to Amazon DocumentDB as a replica set and specify the read preference as secondary preferred

    connection_string = f'mongodb://{db_user}:{db_pass}@127.0.0.1:{port}/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false'
    print(f"Connecting to {connection_string}")
    client = pymongo.MongoClient(connection_string)

    # Specify the database to be used
    db = client.sample_database

    # Specify the collection to be used
    col = db.sample_collection

    # Insert a single document
    col.insert_one({'hello': 'Amazon DocumentDB'})

    # Find the document that was previously written
    x = col.find_one({'hello': 'Amazon DocumentDB'})

    # Print the result to the screen
    print(x)

    # Close the connection
    client.close()
