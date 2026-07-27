with game as (
    select * from {{ ref('slv_dim_game')}}

)
select * from game