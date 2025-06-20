
.PHONY: deploy

deploy:
	git stash
	git pull origin main
	docker compose up -d
