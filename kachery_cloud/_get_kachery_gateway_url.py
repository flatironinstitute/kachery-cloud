import os

_kachery_gateway_url_by_zone = {}

_default_kachery_gateway_url = 'https://kachery-gateway.figurl.org'

def _get_kachery_gateway_url():
    url = os.environ.get('KACHERY_GATEWAY_URL', None)
    if url is not None:
        return url
    kachery_zone = os.environ.get('KACHERY_ZONE', None)
    if kachery_zone is not None:
        if kachery_zone in _kachery_gateway_url_by_zone:
            return _kachery_gateway_url_by_zone[kachery_zone]
        from ._kachery_gateway_request import _kachery_gateway_request
        resp = _kachery_gateway_request({
            'type': 'getZoneInfo',
            'zoneName': kachery_zone
        }, kachery_gateway_url=_default_kachery_gateway_url) # important to use default here so we don't get an infinite recursion
        if resp['found']:
            url = resp['kacheryGatewayUrl']
            _kachery_gateway_url_by_zone[kachery_zone] = url
            return url
        else:
            raise Exception(f'Unrecognized kachery zone: {kachery_zone}')
    return _default_kachery_gateway_url