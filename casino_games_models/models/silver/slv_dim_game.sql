with dim_game as(
    select * from {{ ref('br_dim_game')}}
)
select  
        GAMEID as game_id ,
        GAMETYPE as game_type, 
        parse_json(THEMES) as themes, 
        parse_json(MECHANICS) as mechanics
from    dim_game