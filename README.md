Hyperion Site
=============================================
I. Install GitHub
   1. Register a GitHub account at https://github.com/
   2. Follow the instructions from https://help.github.com/articles/set-up-git to install Git locally
=============================================
II. Clone Repository
    1. Open Terminal application
    2. cd (change directory) into a desired working directory, for example, run 'cd ~/Documents/' to change to the 'Documents' folder
    3. run 'git clone https://github.com/Hongxia/hyperion_site.git'


Development Procedures:
=============================================
1. (optional) python manage.py syncdb - clears database content
2. (optional) python manage.py loaddata Hyperion/fixtures/fixture_*
3. python manage.py runserver 8000