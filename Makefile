run_redis:
	docker-compose --env-file ./nft_loans/configs/.env.dev up redis

run_redis_bg:
	docker-compose --env-file ./nft_loans/configs/.env.dev up redis -d

pre_commit_hooks:
	pre-commit run --all-files

run_celery_beat:
	celery -A nft_loans beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler

run_celery_worker:
	celery -A nft_loans worker --queues=nft_loans_queue -l INFO

run_flower:
	celery -A nft_loans flower --port=${FLOWER_PORT} --basic_auth=${FLOWER_USER}:${FLOWER_PASS} --host=0.0.0.0

run_build_staging:
	docker build -t nft.loans.staging .

run_all_staging:
	docker compose --env-file ./nft_loans/configs/.env.staging up

run_all_staging_downup:
	docker compose --env-file ./nft_loans/configs/.env.staging down && docker compose --env-file ./nft_loans/configs/.env.staging up -d

run_all_staging_local:
	docker compose --env-file ./nft_loans/configs/.env.staging -f docker-compose.local.yaml up

build_staging_image:
	docker build -t nft.loans.staging .
