## Discussion 

- Scalability :
  - Current solution is using a naive iteration relying on DuckDB efficient in memory handling and clumnar access. It is quoted that it can handle dozens of 10M Rows. On my humble laptop it took 5 minutes to process the entire database (including VectorCount and then sorting to he flow)
  - In order to scale up, we can partition data by time ranges or other relevant keys to enable parallel processing. For extreme datasets this can be done by running few instances of the analyser and orchestrating their workloads and aggregating their results
  - Also hosting the service on a docker container would improve deployment consistency and scalability, being able to scale up resources when needed, or to handle increased query loads dynamically.

- Accessing the DB could also be improved by:
  - Adding index to the scheme for faster access
  - Batch reading 
  - Saving itermediate trends.json within the database (compact data sources)

- Additional improvemements and optimizations could include:
  - option for nominal vs normalized delta 
  - per channel distribution
  - keep few sample messages in case the GUI user would like to drill down 
  - using LLM to extract subjects (must have a high frequency load plan for that)


## Dependencies Setup:

- ```conda env create -f environment.yaml -p ./.innohives```
- ```conda activate ./.innohives```

## DB import from csv:
```
CREATE TABLE telegram AS
    SELECT * FROM read_csv_auto(
      'telegram.csv',
      header=true,
      sample_size=-1
    );
```    

