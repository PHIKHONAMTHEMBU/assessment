select 
        casino_id,
        player_id,
        game_id,
        total_spins
from {{ref('slv_fact_activity')}}
where total_spins < 0 -- extract checks for negative spins.