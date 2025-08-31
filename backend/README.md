start db  connection : pg_ctl -D ~/postgres-5433 -o "-p 5433" start
apply db mifgration: alembic revision -m "comment"
 