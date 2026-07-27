
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  select 
        casino_id,
        player_id,
        game_id,
        total_spins
from CASINO_GAMES_DB.SILVER.slv_fact_activity
where total_spins < 0 -- extract checks for negative spins.
  
  
      
    ) dbt_internal_test