from app.modules.core.core_parsing import parse_transactions_to_df
from app.modules.duckdb.duckdb_connection import duck_connection
from app.page.fragments.core_heath_check import get_core_client


class CoreSyncManager:
    @classmethod
    def sync_once(cls) -> bool:
        ...

class CoreSyncTransactionManager(CoreSyncManager):
    @classmethod
    def sync_once(cls, from_scratch: bool = False) -> bool:
        core = get_core_client()
        duck = duck_connection()

        # -----
        # Fetch count

        transaction_count = core.count_transactions()

        #
        # todo -> later on we can launch a couple separate requests to combine?
        transactions = []
        allowed_attempts = 5
        for i in range(allowed_attempts):
            transactions += core.query_transactions(limit=transaction_count, offset=len(transactions))
            if len(transactions) >= transaction_count:
                break

        # -----
        # Parse to polars
        source_df = parse_transactions_to_df(transactions)

        # -----
        # Load into DB
        if from_scratch:
            stmt = """
            SELECT COUNT(*) 
            FROM duckdb_tables 
            WHERE table_name = $table_name
            """
            result = duck.execute(stmt, {"table_name": "hubtransaction"}).fetchone()
            if result[0] > 0:  # If table exists (count > 0), drop it
                duck.execute(f"DROP TABLE hubtransaction")

        # Register the Polars DataFrame, then create
        duck.register("temp_hubtransaction_df", source_df)
        duck.execute(f"CREATE TABLE hubtransaction AS SELECT * FROM temp_hubtransaction_df")

        return True
