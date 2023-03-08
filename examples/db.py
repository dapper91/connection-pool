import psycopg2.extensions

from generic_connection_pool.contrib.psycopg2 import DbConnectionManager
from generic_connection_pool.threding import ConnectionPool

Endpoint = str
Connection = psycopg2.extensions.connection


def main() -> None:
    dsn_params = dict(dbname='postgres', user='postgres', password='secret')

    pool = ConnectionPool[Endpoint, Connection](
        DbConnectionManager(
            dsn_params={
                'master': dict(dsn_params, host='db-master.local'),
                'replica-1': dict(dsn_params, host='db-replica-1.local'),
                'replica-2': dict(dsn_params, host='db-replica-2.local'),
            },
        ),
        acquire_timeout=2.0,
        idle_timeout=60.0,
        max_lifetime=600.0,
        min_idle=3,
        max_size=10,
        total_max_size=15,
        background_collector=True,
    )

    with pool.connection(endpoint='master') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM pg_stats;")
        print(cur.fetchone())

    with pool.connection(endpoint='replica-1') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM pg_stats;")
        print(cur.fetchone())

    pool.close()


main()
