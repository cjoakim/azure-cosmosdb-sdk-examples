## Azure Cosmos DB PostgreSQL API - Design Best Practices

---

## Documentation

### Citus

- https://docs.citusdata.com/en/v12.1/sharding/data_modeling.html
- https://docs.citusdata.com/en/v11.0/develop/api_metadata.html#coordinator-metadata
- https://docs.citusdata.com/en/v12.1/
- https://www.citusdata.com/faq

### Cosmos DB PostgreSQL

- https://learn.microsoft.com/en-us/azure/cosmos-db/postgresql/
- https://github.com/MicrosoftDocs/azure-docs/blob/main/articles/cosmos-db/postgresql/tutorial-design-database-realtime.md

### Azure Database for PostgreSQL

- https://learn.microsoft.com/en-us/azure/postgresql/

---

## General Best Practices

- CosmosDB/PG/Citus are best for **multi tenant** applications
- See the above Citus docs on best practices:
  - **Partition distributed tables by a common tenant_id column**
    - data is horizontally scaled/partitioned
    - high cardinality
    - even distribution
    - do not choose a date or timestamp as the distribution column
  - **Convert small cross-tenant tables to reference tables**
    - these are distributed/copied to all nodes in the cluster
  - **Restrict filter all application queries by tenant_id**

## DDL

```
create_distributed_table("<tablename>", "<sharding-column">)

create_reference_table("<tablename>")

select rebalance_shards("<tablename>")
```

---

## Other Topics

### Star Schema

- Single Fact Table
- Related Dimension Tables 
- https://www.databricks.com/glossary/star-schema
