import os
import time
from decimal import Decimal

import psycopg2
from itemadapter import ItemAdapter

_MAX_RETRIES = 10
_RETRY_DELAY = 3


class DatabasePipeline:
    def open_spider(self, spider):
        db_url = os.environ.get(
            "DATABASE_URL_SYNC",
            "postgresql://postgres:postgres@db:5432/currency_db",
        )
        # Retry loop: Docker DNS for 'db' may not be immediately available
        # when the container starts, even after depends_on: service_healthy.
        for attempt in range(1, _MAX_RETRIES + 1):
            try:
                self.conn = psycopg2.connect(db_url)
                self.cursor = self.conn.cursor()
                self._ensure_tables()
                spider.logger.info(
                    f"Connected to database (attempt {attempt})"
                )
                return
            except psycopg2.OperationalError as exc:
                spider.logger.warning(
                    f"DB connection failed (attempt {attempt}/{_MAX_RETRIES}): {exc}. "
                    f"Retrying in {_RETRY_DELAY}s..."
                )
                time.sleep(_RETRY_DELAY)

        raise RuntimeError(
            f"Could not connect to database after {_MAX_RETRIES} attempts"
        )

    def close_spider(self, spider):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def _ensure_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS currencies (
                id SERIAL PRIMARY KEY,
                char_code VARCHAR(10) UNIQUE NOT NULL,
                num_code VARCHAR(10) NOT NULL,
                name VARCHAR(255) NOT NULL,
                nominal INTEGER NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS exchange_rates (
                id SERIAL PRIMARY KEY,
                currency_id INTEGER NOT NULL REFERENCES currencies(id),
                rate NUMERIC(18, 6) NOT NULL,
                date DATE NOT NULL,
                CONSTRAINT uq_currency_date UNIQUE (currency_id, date)
            )
        """)
        self.conn.commit()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        char_code = adapter.get("char_code")
        num_code = adapter.get("num_code")
        name = adapter.get("name")
        nominal = adapter.get("nominal")
        rate = Decimal(str(adapter.get("rate")))
        rate_date = adapter.get("date")

        self.cursor.execute(
            """
            INSERT INTO currencies (char_code, num_code, name, nominal)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (char_code) DO UPDATE
                SET name = EXCLUDED.name,
                    nominal = EXCLUDED.nominal,
                    num_code = EXCLUDED.num_code
            RETURNING id
            """,
            (char_code, num_code, name, nominal),
        )
        currency_id = self.cursor.fetchone()[0]

        self.cursor.execute(
            """
            INSERT INTO exchange_rates (currency_id, rate, date)
            VALUES (%s, %s, %s)
            ON CONFLICT ON CONSTRAINT uq_currency_date DO UPDATE
                SET rate = EXCLUDED.rate
            """,
            (currency_id, rate, rate_date),
        )
        self.conn.commit()
        return item
