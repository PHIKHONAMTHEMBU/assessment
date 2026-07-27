
  create or replace   view CASINO_GAMES_DB.SILVER.slv_dim_currency
  
  
  
  
  as (
    with dim_currency as (
    select * from CASINO_GAMES_DB.BRONZE.br_dim_currency
)
select 
        CURRENCYID as currency_id, 
        cast(EXCHANGE_RATE_TO_BASE as float) as currency_rate
from    dim_currency
  );

