
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select activity_date
from CASINO_GAMES_DB.GOLD.gl_activity
where activity_date is null



  
  
      
    ) dbt_internal_test