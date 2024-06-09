headers = {
    'sec-ch-ua': '"Android WebView";v="125", "Chromium";v="125", "Not?A_Brand";v="28"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'Accept-Language': 'en-GB,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Host': 'api.hamsterkombat.io',
    'Origin': 'https://hamsterkombat.io',
    'Referer': 'https://hamsterkombat.io/',
    'X-Requested-With': 'org.telegram.messenger',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 9; SM-J530G Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/125.0.6422.72 Mobile Safari/537.36',
}

additional_headers_for_empty_requests = {
    'Accept': '*/*',
    'Content-Length': "0",
}

def createAdditionalHeadersForDataRequests(content_length: int) -> dict:
    return {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Content-Length': str(content_length),
    }
