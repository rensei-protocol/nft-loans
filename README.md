# NFT Loans aggregator backend

## About the project structure
- All project was written with [django](https://docs.djangoproject.com/)
- Database is `postgres`. You can set up postgres db with script in `./db_local` folder.
Please read ReadMe in ./db_local


## Conventions:
- create app names in plural form
- use only single scope for strings: `'` not `"`
- add libs via poetry: `poetry add <package_name>`

## Package management
User `poetry` to add/remove any package from project.
If you add/remove any package, then you must run: `make pre_commit_hooks`; otherwise after the first(1)
attempt to commit, the poetry's pre-hook will override requirements.txt. It means that on the second(2) try of
commit it will be success
> It will help to find the best suitable library and avoid inconsisteny in the future

### Before migrations, must todo:
1. create  migration file, it is very important to run it with app name (otherwise will run globally), e.g:
`./manage.py makemigrations app_name`
2. add migrated file via git: `git add app_name/migrations/migrate_file.py`
3. run migration: `./manage.py migrate app_name`


### Task manager (Celery)
Must to-do:
1. Install all dependencies `poetry install`
2. Migrate celery migrations if they are not migrated yet: `./manage.py migrate`
3. Run redis: `make run_redis` or `make run_redis_bg`
4. In terminal-1 run celery worker command: `make run_celery_worker`. It will run worker in celery
5. In terminal-2 run celery beat command: `make run_celery_beat`. It will run scheduler (beat) in celery
