## Azure Cosmos DB PostgreSQL API - Notes

### Previous Questions

#### 1) Scale out vs Scale up guidance.

**For a Postgres workload, RAM is the key factor.**

In case of a distributed Postgres database, it’s about aggregated RAM, i.e. sum of RAM on all worker nodes. Total RAM needed for workload gives you an idea of the cluster size that would be able to deliver desired performance.

How exactly you’re going to slide and dice the cluster – less nodes with beefier configuration or more nodes with smaller configuration – depends on your experiments / PoC for that specific workload.

Usually you start with somewhat smaller spec for your cluster than you believe is actually needed to see if you can saturate it.
**Then you observe what is exactly reaching 90-100% of utilization, e.g. compute, and scale up that part to repeat the performance runs.**

There’s no universal rule or formula for all workloads, even the ones that are perfect fit for distribution (otherwise we’d have it in our docs).

#### 2) Guidance on TPS expectations

TPS very much depend on specific workload and how good of a fit it is for distribution.

Usually performance PoC gives you an idea of what TPS you can reach with Azure Cosmos DB for PostgreSQL.

#### 3) Monitoring - Key metrics to guide them to scale up

You monitor compute and storage metrics (mostly) and network bandwidth between the app and the cluster.

References:
- [View metrics](https://learn.microsoft.com/en-us/azure/cosmos-db/postgresql/howto-monitoring)
- [Create alerts on metrics](https://learn.microsoft.com/en-us/azure/cosmos-db/postgresql/howto-alert-on-metric)

#### 4) Monitoring - How to integrate with their preferred tooling - Promethius and Grafana

We don’t have integration guidance for these tools.

Usually lookup for guidance of Postgres integration with a tool is a good starting point
for Azure Cosmos DB for PostgreSQL integration with this tool [because we’re running it on PostgreSQL DB engine].

#### 5) Disks and storage - How many IOPS, and is it RAID or clustered

IOPS on its own is not a reliable indicator in case of Azure Cosmos DB for PostgreSQL.

You’d rather want to run the perf PoC I described in #1 to understand what cluster configuration delivers proper performance.

The primary reason for it is that most workloads come from a single node (Postgres or non-Postgres) setup and IOPS in a single node configuration are not exactly the same as IOPs in a distributed Postgres DB. Once you determine the optimal cluster configuration for a workload, you can calculate aggregated IOPS on all worker nodes.

#### 6) Guidance for initial scale settings

See 1) above.
