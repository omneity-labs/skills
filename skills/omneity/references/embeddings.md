# Embeddings and hosted retrieval

Read [the generated API contract](contracts/embeddings.md) for request fields, defaults, auth, and response types.

Use `POST /v1/embeddings` with the public alias `madmon-beta`.

<!-- api-example: post_v1_embeddings application/json -->
```json
{"model":"madmon-beta","input":["first document chunk","second document chunk"]}
```

The response has `data[].embedding`, `data[].index`, `model`, and `usage`.
Map each vector to its input with the returned index. Keep input order stable.
The float output is the portable choice. Do not assume dimensions or limits
from another embedding provider. Read returned vectors and the current model
metadata before creating a vector collection.

Batch independent chunks. Bound the batch by the service limit and payload size.
Cache by model alias and content hash. Keep source IDs, permissions, and chunk
boundaries with each vector. Use the same model for documents and queries.
Re-index when changing the embedding model.

Use `knowledge-search.md` for hosted Khizana retrieval. Use Semango for
self-hosted search. Retrieve relevant chunks before chat. Include source links
and enforce source permissions before synthesis. Read `pricing.md` for units.
