with dim_currency as (
    select * from CASINO_GAMES_DB.BRONZE.br_dim_currency
)
select 
        CURRENCYID as currency_id, 
        cast(EXCHANGE_RATE_TO_BASE as float) as currency_rate
from    dim_currency