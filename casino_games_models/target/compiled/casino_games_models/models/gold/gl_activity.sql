with currency as (
    select * from CASINO_GAMES_DB.SILVER.slv_dim_currency
),
activity as (
    select * from CASINO_GAMES_DB.SILVER.slv_fact_activity
)

select  
        act.activity_date, 
        act.casino_id, 
        act.player_id, 
        act.game_id, 
        act.currency_id,
        act.total_spins, 
        act.golive_date,
        act.total_wager * cur.currency_rate as total_wager_rated, -- converting to provided rates
        act.total_payout * cur.currency_rate as total_payout,   -- converting to provided rates
        (act.total_wager * cur.currency_rate) - act.total_payout * cur.currency_rate as net_wins -- calculating total wins

from    activity act
left outer join 
        currency cur
on      act.currency_id =  cur.currency_id