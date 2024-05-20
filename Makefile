extract:
	pybabel extract --input-dirs=. -o locales/messages.pot

init:
	pybabel init -i locales/messages.pot -d locales -D messages -l uz
	pybabel init -i locales/messages.pot -d locales -D messages -l en
	pybabel init -i locales/messages.pot -d locales -D messages -l kor

compile:
	pybabel compile -d locales -D messages


update:
	pybabel update -d locales -D messages -i locales/messages.pot

admin:
	uvicorn web.app:app --host=localhost --port=8000