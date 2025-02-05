run-local:
	poetry run python ./app/main.py

run-npm-install:
	npm install -g aws-cdk
	cd ./infra;npm install

deploy: run-npm-install
	poetry install
	poetry export -f requirements.txt -o ./app/requirements.txt
	cd ./infra;cdk deploy -c ENV=${ENV} --require-approval never