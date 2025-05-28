import polars as pl


def parse_transactions_to_df(transactions: list[dict]) -> pl.DataFrame:
    """
    @type transactions: list[dict] Parsed to list of transaction dictionaries

    @rtype: pl.DataFrame
    Schema: {
    'interaction': {
        'interaction_uuid': 'bdfbf265704f6ebe617a005584dbc230972b8793311b7ec987fccae528e0822fbafe4934b50d38a4',
        'item_id': 18,
        'item_name': 'Kiesweek voorbeeld Kiesevenement',
        'user_email': 'test@example.com',
        'interaction_type': 100,
        'interaction_id': 178,
        'user_uuid': '129b8b2f-0593-412e-967d-31c1e936194d',
        'last_update_timestamp': '2025-04-30T11:25:51.647536',
        'created_timestamp': '2025-04-30T11:25:51.647536'
        },
    'completed_timestamp': '2025-04-30T11:25:51.700657',
    'created_timestamp': '2025-04-30T11:25:51.647536',
    'transaction_status': 1,
    'note': '',
    'purchased_product': {
        'name': 'Smashburger',
        'description': 'Smashburgers',
        'description_renderer': 0,
        'ordering': 0,
        'blueprint_id': 22,
        'origin_item_id': 18,
        'allow_individualised': False,
        'date_generated': '2025-04-30T11:25:40.956239Z',
        'product_meta': {
            'categorie': 'Te koop!',
            'group': 'Food',
            'other_meta_data': {'form': {'saus': {'type': 'option', 'options': ['Geen', 'Burgersaus', 'Andalouse', 'Ketchup', 'Mayonaise', 'Mammout'], 'value': 'Ketchup'}}}},
            'price_policy': {
                'id': 34,
                'name': None,
                'price': 3.5,
                'ordering': 0
                },
            'note': ''
        },
        'validity': 5,
        'product_blueprint_id': 22,
        'product_blueprint_name': 'Smashburger',
        'price_policy_id': 34,
        'checkout_uuid': '2853e01e-5d5e-4eb8-9e55-0c16d53afcf3'
        }

    """
    base_df = pl.json_normalize(data=transactions, max_level=2)

    # Translating column datatypes and adjusted column names
    adjusted_df = base_df.select(
        pl.col("interaction.interaction_id").alias("interaction_id"),
        pl.col("created_timestamp")
        .str.to_datetime(format="%Y-%m-%dT%H:%M:%S%.f")
        .alias("created_timestamp"),
        pl.col("completed_timestamp")
        .str.to_datetime(format="%Y-%m-%dT%H:%M:%S%.f", strict=False)
        .alias("completed_timestamp"),
        pl.col("product_blueprint_name"),
    )
    return adjusted_df
