
  create or replace   view CASINO_GAMES_DB.BRONZE.br_dim_currency
  
  
  
  
  as (
    SELECT  *
FROM    CASINO_GAMES_DB.RAW.raw_dim_currency
  );

