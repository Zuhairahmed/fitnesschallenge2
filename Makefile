.PHONY: reset_local_sqlite
reset_local_sqlite:
	rm animal_adoption/db.sqlite 
	docker-compose exec \
	-e DATABASE_URL='' \
	backend python animal_adoption/models/initialize_db_data.py

.PHONY: test
test:
	docker-compose exec backend pytest