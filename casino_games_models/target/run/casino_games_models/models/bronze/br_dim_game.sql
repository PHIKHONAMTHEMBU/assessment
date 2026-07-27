
  create or replace   view CASINO_GAMES_DB.BRONZE.br_dim_game
  
  
  
  
  as (
    SELECT  *
FROM    CASINO_GAMES_DB.RAW.raw_dim_game
  );

