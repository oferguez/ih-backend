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