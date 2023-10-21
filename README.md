SizeCarpedia web app.

To deploy in development follow the steps below:
1. Create and fill these files:
    - `docker-compose.override.yml` based on `docker-compose.override-dev.yml`;
    - `web.env` based on `web.env.dev`;
    - `database.env` based on `database.env.dev`;
2. Run `docker-compose build` to build the images and `docker-compose up -d` to start the containers or just use PyCharm's configuration `.run/carpedia_docker_compose_dev.run.xml`;
3. Then wait until the database loads data from the dump and run the following commands:
    - `docker-compose run --rm web python manage.py migrate`;
    - `docker-compose run --rm web python manage.py createsuperuser`;
    - `docker-compose run --rm web python manage.py collectstatic`;
    - `docker-compose restart web`;
4. Now you can access the web app at `http://localhost:8000/` and the admin page at `http://localhost:8000/admin/` (url can be different depending on your configuration).
