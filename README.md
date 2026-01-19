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

## Further features

- option for nominal vs normalized delta 
- per channel distribution
- keep sample messages
