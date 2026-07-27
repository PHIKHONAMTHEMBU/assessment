
  
  create view "dev"."main"."br_dim-currency__dbt_tmp" as (
    SELECT  *
FROM    read_csv_auto('casino_games_models\seeds\dim_currency.csv', delim=';', header=True)
  );
