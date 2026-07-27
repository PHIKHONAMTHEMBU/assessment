with slv_fact_activity as (
    select * from {{ ref('br_fact_activity')}}

)
select  
        
        CASINOID as casino_id,
        PLAYERID as player_id,
        GAMEID as game_id,
        CURRENCYID as currency_id, 

        -- handling transformation of financial data
        cast(TOTALWAGER as float) as total_wager, 
        cast(TOTALPAYOUT as float) as total_payout,
        cast(TOTALSPINS as integer) as total_spins,
        
        -- converting dates  
        coalesce(
        try_to_date(trim(replace(GOLIVE_DATE, '"', '')), 'YYYY/MM/DD'),
        try_to_date(trim(replace(GOLIVE_DATE, '"', '')), 'YYYY-MM-DD')
    ) as golive_date,
        coalesce(
        try_to_date(trim(replace(date, '"', '')), 'YYYY/MM/DD'),
        try_to_date(trim(replace(date, '"', '')), 'YYYY-MM-DD')
    ) as activity_date
from    slv_fact_activity