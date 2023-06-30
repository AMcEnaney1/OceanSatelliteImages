## Aidan McEnaney
## June 30th, 2023
## Python file to do config


from sentinelhub import SHConfig
import keys

# Setting up config
config = SHConfig()
config.sh_client_id = keys.client_id
config.sh_client_secret = keys.client_secret