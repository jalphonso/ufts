# -*- coding: utf-8 -*-
#
# Copyright 2013 SSH Communication Security Corporation.
# All rights reserved.
# This software is protected by international copyright laws.
#

"""
Utility functions for handling certificates
"""

def _dictify_dn(dn):
    return dict(x.split('=') for x in dn.split('/') if '=' in x)

def user_dict_from_dn(dn):
    d = _dictify_dn(dn)
    ret = dict()
    try:
        ret['username'] = d['1.2.3.4.5.6.7.8'] #userName OID
    except KeyError:
        ret['username'] = None
    try:
        ret['first_name'], ret['last_name'] = d['CN'].title().split()
    except ValueError:
        ret['first_name'] = ''
        ret['last_name'] = d['CN'].title()
    except KeyError:
        ret['first_name'] = ''
        ret['last_name'] = ''
    try:
        ret['email'] = d['emailAddress']
    except KeyError:
        ret['email'] = ''
    return ret
