

SELECT  *
FROM    {{ source('casino_activity_games', 'raw_dim_currency')}}