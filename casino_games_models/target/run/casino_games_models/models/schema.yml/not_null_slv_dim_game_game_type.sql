
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select game_type
from CASINO_GAMES_DB.SILVER.slv_dim_game
where game_type is null



  
  
      
    ) dbt_internal_test