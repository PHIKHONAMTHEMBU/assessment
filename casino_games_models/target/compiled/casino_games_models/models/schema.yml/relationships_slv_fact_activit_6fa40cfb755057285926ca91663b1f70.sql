
    
    

with child as (
    select game_id as from_field
    from CASINO_GAMES_DB.SILVER.slv_fact_activity
    where game_id is not null
),

parent as (
    select game_id as to_field
    from CASINO_GAMES_DB.SILVER.slv_dim_game
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


