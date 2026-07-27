
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select currency_id
from CASINO_GAMES_DB.GOLD.gl_activity
where currency_id is null



  
  
      
    ) dbt_internal_test