
  
  create view "dev"."main"."br_dim-game__dbt_tmp" as (
    SELECT  *
FROM    read_csv_auto('casino_games_models\seeds\dim_game.csv', delim=';', header=True)
  );
