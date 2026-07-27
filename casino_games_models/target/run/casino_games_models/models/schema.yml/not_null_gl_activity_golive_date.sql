
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select golive_date
from CASINO_GAMES_DB.GOLD.gl_activity
where golive_date is null



  
  
      
    ) dbt_internal_test