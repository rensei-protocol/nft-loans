run_redis:
	docker-compose --env-file ./nft_loans/configs/.env.dev.local up redis

run_redis_bg:
	docker-compose --env-file ./nft_loans/configs/.env.dev.local up redis -d

pre_commit_hooks:
	pre-commit run --all-files

run_celery_beat:
	celery -A nft_loans beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler

run_celery_worker:
	celery -A nft_loans worker --queues=nft_loans_queue -l INFO
