SELECT  *
FROM    {{ source('casino_activity_games', 'raw_fact_activity')}}