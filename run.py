import os
from app import create_app

environment = os.environ.get('FLASK_ENV', 'development')
application = create_app(environment)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    application.run(host='0.0.0.0', port=port, debug=True)
