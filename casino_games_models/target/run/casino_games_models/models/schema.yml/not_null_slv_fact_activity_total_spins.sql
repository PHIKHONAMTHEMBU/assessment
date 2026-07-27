
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select total_spins
from CASINO_GAMES_DB.SILVER.slv_fact_activity
where total_spins is null



  
  
      
    ) dbt_internal_test