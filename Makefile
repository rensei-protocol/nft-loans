run_redis:
	docker-compose --env-file ./nft_loans/configs/.env.dev.local up redis

run_redis_bg:
	docker-compose --env-file ./nft_loans/configs/.env.dev.local up redis -d

pre_commit_hooks:
	pre-commit run --all-files
