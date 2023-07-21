## Aidan McEnaney
## June 30th, 2023
## Python file to do config


from sentinelhub import SHConfig
from sentinelsat import SentinelAPI
import keys

## Comment out api's config if you are not using it

# Setting up config for SentinelHub
config = SHConfig()
config.sh_client_id = keys.client_id
config.sh_client_secret = keys.client_secret

# Setting up config for Sentinelsat
api = SentinelAPI(keys.username_sensat, keys.password_sensat)