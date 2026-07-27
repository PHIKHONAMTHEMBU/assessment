
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select casino_id
from CASINO_GAMES_DB.SILVER.slv_fact_activity
where casino_id is null



  
  
      
    ) dbt_internal_test