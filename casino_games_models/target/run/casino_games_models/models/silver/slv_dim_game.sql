
  create or replace   view CASINO_GAMES_DB.SILVER.slv_dim_game
  
  
  
  
  as (
    with dim_game as(
    select * from CASINO_GAMES_DB.BRONZE.br_dim_game
)
select  
        GAMEID as game_id ,
        GAMETYPE as game_type, 
        parse_json(THEMES) as themes, 
        parse_json(MECHANICS) as mechanics
from    dim_game
  );

