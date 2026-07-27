
    
    

select
    game_id as unique_field,
    count(*) as n_records

from CASINO_GAMES_DB.SILVER.slv_dim_game
where game_id is not null
group by game_id
having count(*) > 1


