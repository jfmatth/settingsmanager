import logging.config

LOG_SETTINGS = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'detailed',
#            'stream': 'ext://sys.stdout',
        },
                 
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'detailed',
            'filename': 'junk.log',
            'mode': 'a',
            'maxBytes': 10485760,
            'backupCount': 5,
        },
    
    },
    'formatters': {
        'detailed': {
            'format': '%(asctime)s %(module)-17s line:%(lineno)-4d ' \
            '%(levelname)-8s %(message)s',
        },
        'email': {
            'format': 'Timestamp: %(asctime)s\nModule: %(module)s\n' \
            'Line: %(lineno)d\nMessage: %(message)s',
        },
    },
    'loggers': {
        'settings': {
            'level':'DEBUG',
            'handlers': ['file','console'],
            },
        'main': {
            'level':'INFO',
            'handlers': ['file','console'],
            },

    }
}

logging.config.dictConfig(LOG_SETTINGS)