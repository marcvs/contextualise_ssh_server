#!/bin/bash

dh_patch_pam_ssh_config() {
    CONFIG="/etc/pam.d/sshd"
    # Check if there is already a backup of the pam config:
    test -e ${CONFIG}.orig || cp ${CONFIG} ${CONFIG}.orig

    # Check if pam-ssh-oidc is already enabled:
    cat ${CONFIG} | grep -v ^# | grep -q  "pam_oidc_token.so" && {
        echo "### pam-ssh-oidc is already configured. Nothing to do ###"
    }
    cat ${CONFIG} | grep -v ^# | grep -q  "pam_oidc_token.so" || {
        echo "######################################################################"
        echo "#  Enabling configuration for pam_oidc_token.so in ${CONFIG}"
        echo "#  A backup is in ${CONFIG}.dist"
        echo "######################################################################"
        test -e ${CONFIG}.dist && mv ${CONFIG}.dist /tmp
        HEADLINE=`head -n 1 ${CONFIG}`
        mv ${CONFIG} ${CONFIG}.dist
        echo ${HEADLINE} > ${CONFIG}
        echo "" >> ${CONFIG}
        echo "# use pam-ssh-oidc" >> ${CONFIG}
        echo "auth   sufficient pam_oidc_token.so config=/etc/pam.d/pam-ssh-oidc-config.ini" >> ${CONFIG}
        cat ${CONFIG}.dist | grep -v "${HEADLINE}" >> ${CONFIG}
    }
}

dh_patch_pam_ssh_config
