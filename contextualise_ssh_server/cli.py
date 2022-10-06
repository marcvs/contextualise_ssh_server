"""Console script for contextualise_ssh_server."""
import logging
import logsetup
import sys

from jinja2 import Template
import jinja2
import os

from config import CONFIG
from parse_args import args
from flaat import BaseFlaat

logger = logging.getLogger(__name__)
TRUSTED_OP_LIST = [
    "https://b2access.eudat.eu/oauth2/",
    "https://b2access-integration.fz-juelich.de/oauth2",
    "https://unity.helmholtz-data-federation.de/oauth2/",
    "https://login.helmholtz-data-federation.de/oauth2/",
    "https://login-dev.helmholtz.de/oauth2/",
    "https://login.helmholtz.de/oauth2/",
    "https://unity.eudat-aai.fz-juelich.de/oauth2/",
    "https://services.humanbrainproject.eu/oidc/",
    "https://accounts.google.com/",
    "https://aai.egi.eu/oidc/",
    "https://aai.egi.eu/auth/realms/egi",
    "https://aai-demo.egi.eu/auth/realms/egi",
    "https://aai-demo.egi.eu/oidc/",
    "https://aai-dev.egi.eu/oidc/",
    "https://aai-dev.egi.eu/auth/realms/egi",
    "https://login.elixir-czech.org/oidc/",
    "https://iam-test.indigo-datacloud.eu/",
    "https://iam.deep-hybrid-datacloud.eu/",
    "https://iam.extreme-datacloud.eu/",
    "https://oidc.scc.kit.edu/auth/realms/kit/",
    "https://proxy.demo.eduteams.org",
    "https://wlcg.cloud.cnaf.infn.it/",
]


def get_flaat(trusted_op_list=[]):
    flaat = BaseFlaat()

    trusted_op_list = [
        x for x in CONFIG.get("trust", "trusted_op_list").split("\n") if x != ""
    ]
    if trusted_op_list is not None:
        flaat.set_trusted_OP_list(trusted_op_list)
    else:
        flaat.set_trusted_OP_list(TRUSTED_OP_LIST)
        logger.warning(f"Using hardcoded trusted OP list")

    # flaat.set_verbosity(0, set_global =False)
    return flaat


def render_template(template_file_in, template_file_out, config):
    """Render config template to config file"""
    with open(template_file_in, "r") as fh:
        template_data = fh.read()
    template = Template(template_data)
    try:
        config_file_content = template.render(config)
        with open(template_file_out, "w") as fp:
            fp.write(config_file_content)
        os.chmod(template_file_out, 0o644)
    except jinja2.exceptions.UndefinedError as e:
        logger.error(
            f"did not find variables for template file {template_file_out}: {e}"
        )


def main():
    """Console script for contextualise_ssh_server."""

    flaat = get_flaat()
    user_infos = flaat.get_user_infos_from_access_token(args.access_token[0])
    if user_infos is None:
        logger.error("Failed to get userinfos for the provided access token")
        sys.exit(1)

    # Determine authorised VOs:
    # all my VOs:
    vo_list = user_infos.get("eduperson_entitlement")

    # overwritten by environment variable:
    temp = os.getenv("SSH_AUTHORISE_VOS")
    if temp is not None:
        vo_list = temp

    # emptied if not necessary
    temp = os.getenv("SSH_AUTHORISE_OTHERS_IN_MY_VO")
    if temp is None:
        vo_list = []

    # collect data for motley_cue.conf
    mc_config = {"user_sub": user_infos.get("sub"),
                 "user_iss": user_infos.get("iss"),
                 "vo_list": vo_list}

    # render motley-cue.conf:
    mc_template = CONFIG.get(
        "templates", "motley_cue.conf", fallback="motley_cue.template.conf"
    )
    mc_output = "rendered_motley_cue.conf"
    render_template(mc_template, mc_output, mc_config)

    # collect data for feudal_adapter.conf
    asr = CONFIG.get("users", "assurance",
                            fallback="profile/cappuccino")
    asr = [x for x in asr.split("\n") if x != ""]
    assurance = "\n    ".join(asr)

    fa_config = {
        "assurance_prefix": CONFIG.get("users", "assurance_prefx",
                            fallback="https://refeds.org/assurance/"),
        "assurance":        assurance,
        "shell":            CONFIG.get("users", "shell",
                            fallback="/bin/bash"),
        "username_mode":    CONFIG.get("users", "username_mode",
                            fallback="friendly"),
        "primary_group":    CONFIG.get("users", "primary_group",
                            fallback="cool"),
        "":            CONFIG.get("users", "",
                            fallback=""),
    }
    # render feudal_adapter.conf:
    fa_template = CONFIG.get(
        "templates", "feudal_adapter.conf", fallback="feudal_adapter.template.conf"
    )
    fa_output = "rendered_feudal_adapter.conf"
    render_template(fa_template, fa_output, fa_config)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
