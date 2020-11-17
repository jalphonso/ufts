# -*- coding: utf-8 -*-
#
# Copyright 2013 SSH Communication Security Corporation.
# All rights reserved.
# This software is protected by international copyright laws.
#

"""
Utility functions for handling certificates
"""

import logging

logging.basicConfig()
logger = logging.getLogger(__name__)


def _dictify_dn(dn):
    return dict(x.split('=') for x in dn.split('/') if '=' in x)

def user_dict_from_dn(dn):
    """
    DN Example
      /C=US/ST=Maryland/O=ufts/CN=first last middle userid/emailAddress=user@email.org

    Supported CN formats are
      lastname username
      lastname firstname username
      lastname firstname middlename username
    """

    logger.debug("Cert incoming DN: {0}".format(dn))
    d = _dictify_dn(dn)
    ret = dict()
    try:
        full_name, ret['username'] = d['CN'].rsplit(' ', 1)
        logger.debug(full_name)
        full_name = full_name.title().split()
        logger.debug(full_name)
        if len(full_name) == 3:
            # middle name is not a field in the user model so we ignore it
            ret['last_name'], ret['first_name'], middle_name = full_name
        elif len(full_name) == 2:
            ret['last_name'], ret['first_name'] = full_name
        elif len(full_name) == 1:
            ret['last_name'] = full_name
        else:
            raise ValueError
    except (ValueError, KeyError):
        logger.error("Unsupported DN/CN format {0}".format(dn))
        ret['username'] = ''

    try:
        ret['email'] = d['emailAddress']
    except KeyError:
        ret['email'] = ''
    return ret
