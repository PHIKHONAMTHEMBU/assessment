
  
    

create or replace transient table CASINO_GAMES_DB.GOLD.gl_game
    
    
    
    
    

    as (with game as (
    select * from CASINO_GAMES_DB.SILVER.slv_dim_game

)
select * from game
    )
;


  