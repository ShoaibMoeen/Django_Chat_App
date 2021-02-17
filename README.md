# Django_Chat_App


This project demonstrate django one to one chat with authentication using django channels 3 and redis.

How to run
1. Clone the repo
2. Run requirements.txt
3. Install redis on your windows if not installed and restart
4. Change database configuration to your database
5. Migrate the database
6. Run on local server


How to add chat function on your project
1. Run requirements.txt
2. Create a chat app
3. Copy consumer.py, routing.py, templates, views, urls and models from this project.
4. Copy the configuration in asgi file
5. Change the settings:
  1. Add channels and chat in installed apps
  2. Set ASGI_APPLICATION = 'yourproject.asgi.application'
  3. Set Channel Layers in the settings
6. Migrate and run the project and you can access the chat feature on the provided url


For more information visit https://channels.readthedocs.io/en/stable/

PS: You will need to add Heroku-redis add-on on your heroku app to run the application
