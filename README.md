[![PyPI Badge](https://img.shields.io/pypi/v/contextualise_ssh_server.svg)](https://pypi.python.org/pypi/contextualise_ssh_server)
[![Read the Docs](https://readthedocs.org/projects/contextualise-ssh-server/badge/?version=latest)](https://contextualise-ssh-server.readthedocs.io/en/latest/?version=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# contextualise-ssh-server

Contextualise motley-cue and pam-ssh-oidc on a VM Server

## Installation

contextualise-ssh-server is available on [PyPI](https://pypi.org/project/contextualise_ssh_server/). Install using `pip`:

```bash
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

# PAM

For enabling and disabling tokens in pam, you can use the scripts
`enable-pam-ssh.sh` and `disable-pam-ssh.sh`

They are installed into the same folder as the python file, which you can
find with ` contextualise_ssh_server -b`

# VM Integration

## Install packages to VM image:

```
yum install motley-cue pam-ssh-oidc
```

## Include this in the VM startup:

```
# enable tokens in pam:
`contextualise_ssh_server -b`/enable-pam-ssh.sh

# create motley-cue config
cd /tmp
contextualise_ssh_server $USER_OIDC_ACCESS_TOKEN

# place them in /etc/motley_cue/ 
sudo cat motley_cue.conf     > /etc/motley_cue/motley_cue.conf
sudo cat feudal_adapter.conf > /etc/motley_cue/feudal_adapter.conf
```
