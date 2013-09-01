from gluon.storage import Storage
settings = Storage()

settings.enabled = True  # As a security measure set to False when finished with.

settings.migrate = True
settings.title = 'WebSetup Sahana Eden'
settings.subtitle = 'Sahana Eden'
settings.author = ''
settings.author_email = ''
settings.keywords = 'WebSetup Sahana Eden'
settings.description = 'Web setup for Sahana Eden'
settings.layout_theme = 'TinyBlue'
settings.database_uri = 'sqlite://storage.sqlite'
settings.security_key = '07fdb316-744b-48e5-a9d4-bdec76461215'
settings.email_server = 'logging'
settings.email_sender = ''
settings.email_login = ''
settings.login_method = 'local'
settings.login_config = ''
settings.plugins = []
