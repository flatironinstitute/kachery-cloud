# Kachery gateway cost estimate

## Estimate based on number of uploads/downloads and storage

All prices below are per month unless otherwise specified.

Let `U` be the total number in millions of files uploaded to the gateway per month.

Let `D` be the total number in millions of non-cached download requests per month.

Based on the below breakdown, the estimated cost per month would be

```
$20 + ($6.15)U + ($4.02)D 
```

assuming that `D + 2U < 14`.

So, for example, if your gateway receives one upload request and one non-cached download request every second of every day (~2.5 million per month), the total cost would be approximately $45 per month.

On the other hand, if your gateway has only 100,000 uploads and 100,000 non-cached downloads per month, the cost would be approximately $21 per month.

## Vercel Serverless API

`$20/user` (only 1 user needed)

`1 TB` bandwidth included - but we would never expect to come close to that since none of the actual data files are sent through Vercel.

`1000 GB-hours` of serverless function execution included. The number of requests is on the order of `D + 2U` million. If we assume `250ms` per request and `1GB` RAM allocated, then we are allotted around `14 million` function calls for free. After that it gets a lot more expensive `$400 per 1000 GB-hours`. So if it gets that point, we'd want to arrange for custom pricing and an enterprise account.

If we are below the threshold of `D + 2U < 14` then the total cost per month for the Vercel service is
```
$20 assuming D + 2U < 14
```

## MongoDB Atlas Serverless Database

Each upload results in around 1 read operation and 1 write operation.

Each non-cached download results in around 2 read operations and 2 write operations.

The cost of one million read operations ranges between `$0.09` and `$0.22` depending on the daily volume (let's estimate it at `$0.15`).

The cost of one million write operations ranges between `$0.90` and `$2.20` depending on the daily volume (let's estimate it at `1.50`).

So the estimated cost per month would be

```
($1.65)U + ($3.30)D
```
