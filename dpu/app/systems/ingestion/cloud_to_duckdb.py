import polars as pl
from azure.storage.blob import BlobProperties
from azure.storage.blob.aio import ContainerClient


class CloudSyncManager:
    @classmethod
    async def fetch_data_count(cls, container_client: ContainerClient, name_starts_with: str = "") -> int:
        count = 0
        async for _ in container_client.list_blob_names(name_starts_with=name_starts_with):
            count += 1
        return count

    @classmethod
    async def fetch_data(cls, container_client: ContainerClient,
                   **kwargs) -> list[dict]:
        properties = []
        async for blob in container_client.list_blobs():
            blob: BlobProperties
            properties.append({key: value for key, value in blob.items()})
        return properties

    @classmethod
    def parse_to_df(cls, input_list: list[dict], **kwargs):
        """
        {
            'name': '2-Matlab_scripts.pdf',
            'container': 'ingenium-cloud',
            'snapshot': None,
            'version_id': None,
            'is_current_version': None,
            'blob_type': <BlobType.BLOCKBLOB: 'BlockBlob'>,
            'metadata': {},
            'encrypted_metadata': None,
            'last_modified': datetime.datetime(2025, 6, 3, 15, 23, 49, tzinfo=datetime.timezone.utc),
            'etag': '0x8DDA2B2A3FD1C28',
            'size': 274767,
            'content_range': None,
            'append_blob_committed_block_count': None,
            'is_append_blob_sealed': None,
            'page_blob_sequence_number': None,
            'server_encrypted': True,
            'copy': {
                'id': None,
                'source': None,
                'status': None,
                'progress': None,
                'completion_time': None,
                'status_description': None,
                'incremental_copy': None,
                'destination_snapshot': None
                },
            'content_settings': {
                'content_type': 'application/pdf',
                'content_encoding': None,
                'content_language': None,
                'content_md5': bytearray(b"\x07/\xf5\x1cx\xb5\xe3\xe4\'al~DW\x9c\xff"),
                'content_disposition': None,
                'cache_control': None
                },
            'lease': {
                'status': 'unlocked',
                'state': 'available',
                'duration': None
                },
            'blob_tier': 'Hot',
            'rehydrate_priority': None,
            'blob_tier_change_time': None,
            'blob_tier_inferred': True,
            'deleted': None,
            'deleted_time': None,
            'remaining_retention_days': None,
            'creation_time': datetime.datetime(2025, 6, 3, 15, 23, 49, tzinfo=datetime.timezone.utc),
            'archive_status': None,
            'encryption_key_sha256': None,
            'encryption_scope': None,
            'request_server_encrypted': None,
            'object_replication_source_properties': [],
            'object_replication_destination_policy': None,
            'last_accessed_on': None,
            'tag_count': None,
            'tags': None,
            'immutability_policy': {
                'expiry_time': None,
                'policy_mode': None},
                'has_legal_hold': None,
                'has_versions_only': None
                }
        """
        return pl.from_dicts(input_list).select(
            'name', 'last_modified', 'creation_time', 'last_accessed_on'
        )

    @classmethod
    async def sync_once(cls,
                  container_client: ContainerClient,
                  from_scratch: bool = False,
                  query_blob_properties: bool = True):

        # -----
        # Fetch count
        count_in_blob = await cls.fetch_data_count(container_client=container_client)

        # ---
        # Fetch blobs
        fetched_data: list[dict] = await cls.fetch_data(container_client=container_client)

        # ---
        # Parse to df
        source_df = cls.parse_to_df(fetched_data)

        # -----
        # Load into DB
        # table = "cloudblob"
        # if from_scratch:
        #     stmt = (
        #         """SELECT COUNT(*) FROM duckdb_tables WHERE table_name = $table_name"""
        #     )
        #     result = duck.execute(stmt, {"table_name": table}).fetchone()
        #     if result[0] > 0:  # If table exists (count > 0), drop it
        #         duck.execute(f"""DROP TABLE {table}""")
        #
        #
        # # Register the Polars DataFrame, then create
        # duck.register(f"temp_{table}_df", source_df)
        # duck.execute(
        #     f"CREATE TABLE {table} AS SELECT * FROM temp_{table}_df"
        # )

        return True
