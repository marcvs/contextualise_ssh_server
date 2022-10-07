#!/bin/bash

dh_unpatch_pam_ssh_config() {
    CONFIG="/etc/pam.d/sshd"
    test -e ${CONFIG}.orig && cat ${CONFIG}.orig > ${CONFIG}
}

dh_unpatch_pam_ssh_config
