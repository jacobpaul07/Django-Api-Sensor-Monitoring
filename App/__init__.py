import os
if os.environ.get('RUN_MAIN', None) != 'true':
    default_app_config = 'sih_python_django.myAppConfig.MyAppConfig'