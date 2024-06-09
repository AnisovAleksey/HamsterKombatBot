import random

from bot.utils.scripts import generate_random_visitor_id


visitor_id = generate_random_visitor_id()

timezones = {
    'America/New_York': 'en-US',
    'America/Los_Angeles': 'en-US',
    'Europe/London': 'en-GB',
    'Europe/Paris': 'fr-FR',
    'Europe/Berlin': 'de-DE',
    'Asia/Tokyo': 'ja-JP',
    'Asia/Shanghai': 'zh-CN',
    'Asia/Kolkata': 'hi-IN',
    'Australia/Sydney': 'en-AU',
    'Africa/Johannesburg': 'en-ZA',
    'America/Sao_Paulo': 'pt-BR',
    'America/Mexico_City': 'es-MX',
    'Europe/Moscow': 'ru-RU',
    'Asia/Dubai': 'ar-AE',
    'Pacific/Auckland': 'en-NZ'
}

timezone = random.choice(list(timezones.keys()))
language = timezones[timezone]

FINGERPRINT = {
    'fingerprint': {
        'version': '4.2.1',
        'visitorId': generate_random_visitor_id(),
        'components': {
        'fonts': {
            'value': [
            'sans-serif-thin'
            ],
            'duration': random.randint(115, 245)
        },
        'domBlockers': {
            'value': [],
            'duration': random.randint(65, 245)
        },
        'fontPreferences': {
            'value': {
            'default': 145.90625,
            'apple': 145.90625,
            'serif': 164.71875,
            'sans': 145.90625,
            'mono': 132.625,
            'min': 72.953125,
            'system': 145.90625
            },
            'duration': random.randint(22, 52)
        },
        'audio': {
            'value': 0.00007444995,
            'duration': random.randint(54, 112)
        },
        'screenFrame': {
            'value': [
            0,
            0,
            0,
            0
            ],
            'duration': randint(2, 7)
        },
        'canvas': None,
        'osCpu': {
            'duration': 0
        },
        'languages': {
            'value': [
            [
                'ru'
            ]
            ],
            'duration': random.randint(1, 3)
        },
        'colorDepth': {
            'value': 24,
            'duration': 1
        },
        'deviceMemory': {
            'value': 4,
            'duration': 0
        },
        'screenResolution': {
            'value': [
            640,
            360
            ],
            'duration': 1
        },
        'hardwareConcurrency': {
            'value': 4,
            'duration': 1
        },
        'timezone': {
            'value': 'Europe/Moscow',
            'duration': random.randint(45, 65)
        },
        'sessionStorage': {
            'value': True,
            'duration': 0
        },
        'localStorage': {
            'value': True,
            'duration': 1
        },
        'indexedDB': {
            'value': True,
            'duration': 3
        },
        'openDatabase': {
            'value': True,
            'duration': 1
        },
        'cpuClass': {
            'duration': 0
        },
        'platform': {
            'value': 'Linux aarch64',
            'duration': 0
        },
        'plugins': {
            'value': [],
            'duration': 1
        },
        'touchSupport': {
            'value': {
            'maxTouchPoints': random.randint(3, 10),
            'touchEvent': True,
            'touchStart': True
            },
            'duration': 1
        },
        'vendor': {
            'value': 'Google Inc.',
            'duration': 0
        },
        'vendorFlavors': {
            'value': [],
            'duration': 1
        },
        'cookiesEnabled': {
            'value': True,
            'duration': 11
        },
        'colorGamut': {
            'value': 'srgb',
            'duration': 0
        },
        'invertedColors': {
            'duration': 1
        },
        'forcedColors': {
            'value': False,
            'duration': 0
        },
        'monochrome': {
            'value': 0,
            'duration': 1
        },
        'contrast': {
            'value': 0,
            'duration': 4
        },
        'reducedMotion': {
            'value': False,
            'duration': 1
        },
        'reducedTransparency': {
            'value': False,
            'duration': 0
        },
        'hdr': {
            'value': False,
            'duration': 0
        },
        'math': {
            'value': {
            'acos': 1.4473588658278522,
            'acosh': 709.889355822726,
            'acoshPf': 355.291251501643,
            'asin': 0.12343746096704435,
            'asinh': 0.881373587019543,
            'asinhPf': 0.8813735870195429,
            'atanh': 0.5493061443340548,
            'atanhPf': 0.5493061443340548,
            'atan': 0.4636476090008061,
            'sin': 0.8178819121159085,
            'sinh': 1.1752011936438014,
            'sinhPf': 2.534342107873324,
            'cos': -0.8390715290095377,
            'cosh': 1.5430806348152437,
            'coshPf': 1.5430806348152437,
            'tan': -1.4214488238747245,
            'tanh': 0.7615941559557649,
            'tanhPf': 0.7615941559557649,
            'exp': 2.718281828459045,
            'expm1': 1.718281828459045,
            'expm1Pf': 1.718281828459045,
            'log1p': 2.3978952727983707,
            'log1pPf': 2.3978952727983707,
            'powPI': 1.9275814160560204e-50
            },
            'duration': 4
        },
        'pdfViewerEnabled': {
            'value': False,
            'duration': 2
        },
        'architecture': {
            'value': 127,
            'duration': 0
        },
        'applePay': {
            'value': -1,
            'duration': 1
        },
        'privateClickMeasurement': {
            'duration': 0
        },
        'webGlBasics': {
            'value': {
            'version': 'WebGL 1.0 (OpenGL ES 2.0 Chromium)',
            'vendor': 'WebKit',
            'vendorUnmasked': 'Qualcomm',
            'renderer': 'WebKit WebGL',
            'rendererUnmasked': 'Adreno (TM) 530',
            'shadingLanguageVersion': 'WebGL GLSL ES 1.0 (OpenGL ES GLSL ES 1.0 Chromium)'
            },
            'duration': random.randint(3, 10)
        },
        'webGlExtensions': None
        }
    }
}
