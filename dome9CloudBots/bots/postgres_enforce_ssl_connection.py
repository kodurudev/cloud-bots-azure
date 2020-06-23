from azure.common.credentials import ServicePrincipalCredentials
import logging
import os
from azure.mgmt.rdbms.postgresql import PostgreSQLManagementClient
from msrestazure.azure_exceptions import CloudError
from azure.mgmt.rdbms.postgresql.models import ServerUpdateParameters

# Set Azure AD credentials from the environment variables
credentials = ServicePrincipalCredentials(
    client_id=os.environ['CLIENT_ID'],
    secret=os.environ['SECRET'],
    tenant=os.environ['TENANT']
)

def raise_credentials_error():
    msg = 'Error! Subscription id or credentials are missing.'
    logging.info(f'{__file__} - {msg}')
    return msg

def run_action(credentials, rule, entity, params):
    logging.info(f'{__file__} - ${run_action.__name__} started')
    server_name = entity['name']
    subscription_id = entity['accountNumber']
    group_name = entity['resourceGroup']
    logging.info(
        f'{__file__} - subscription_id : {subscription_id} - group_name : {group_name} - server_name : {server_name}')

    if not subscription_id or not credentials:
        return raise_credentials_error()

    try:
        db_client = PostgreSQLManagementClient(credentials, subscription_id)
        db_client.servers.update(group_name, 
                                 server_name, 
                                 ServerUpdateParameters(ssl_enforcement='Enabled'))   
        msg = f'Force SSL connection was enabled successfully on PostgreSQL server: {server_name}'
        logging.info(f'{__file__} - {msg}')
        return f'{msg}'

    except CloudError as e:
        msg = f'Unexpected error : {e.message}'
        logging.info(f'{__file__} - {msg}')
        return msg
    