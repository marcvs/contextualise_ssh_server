[![PyPI Badge](https://img.shields.io/pypi/v/contextualise_ssh_server.svg)](https://pypi.python.org/pypi/contextualise_ssh_server)
[![Read the Docs](https://readthedocs.org/projects/contextualise-ssh-server/badge/?version=latest)](https://contextualise-ssh-server.readthedocs.io/en/latest/?version=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# contextualise-ssh-server
Contextualise motley-cue and pam-ssh-oidc on a VM Server

## Installation
contextualise-ssh-server is available on [PyPI](https://pypi.org/project/contextualise_ssh_server/). Install using `pip`:
```
pip install contextualise_ssh_server
```


# Configuration

Config is read from `/etc/contextualise_ssh_server.conf` 

There is a default config file in the place where pip installs this package

There you will also find templates for motley_cue.conf and feudal_adapter.conf


## Environment Variables

These control the behaviour:

- `SSH_AUTHORISE_OTHERS_IN_MY_VO`: If set to a nonempty value ALL members of
    ALL VOs of the user will be authorised to log in.


- `SSH_AUTHORISE_VOS`: If the above variable is not set and this variable
    specifies a json list of VOs (actually AARC-G069/G027 Entitlements) to
    authorise. 

    Example:
    `export SSH_AUTHORISE_VOS="['urn:mace:egi.eu:group:cryoem.instruct-eric.eu:admins:role=owner#aai.egi.eu', 'urn:mace:egi.eu:group:umsa.cerit-sc.cz:admins:role=owner#aai.egi.eu']`

# Usage

The tools will output the two config files `motley_cue.conf` and
`feudal_adapter.conf` in the folder in which it is called.

Those need to be placed in `/etc/motley_cue` with the access token of the
user as the only parameter:

`contextualise_ssh_server <OIDC_ACCESS_TOKEN>`
