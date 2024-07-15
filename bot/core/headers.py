# pylint: disable=C0301
import json as json_parser

headers = {
    'Accept-Language': 'en-GB,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Host': 'api.hamsterkombatgame.io',
    'Origin': 'https://hamsterkombatgame.io',
    'Referer': 'https://hamsterkombatgame.io/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
}

additional_headers_for_empty_requests = {
    'Accept': '*/*',
    'Content-Length': "0",
}


def create_headers(json: dict | None) -> dict:
    if json is None:
        return additional_headers_for_empty_requests
    return {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Content-Length': str(len(json_parser.dumps(json).encode('utf-8'))),
    }
