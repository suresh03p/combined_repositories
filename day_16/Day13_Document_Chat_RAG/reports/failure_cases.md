# Failure Cases

| Case | Expected behavior |
|---|---|
| Empty PDF | `Document contains no readable text.` |
| `image.exe` | `Unsupported file type.` |
| Duplicate document | `Document already exists.` |
| No relevant information | `Information not found in the uploaded documents.` |
| Vector database unavailable | `Unable to retrieve documents. Please try again.` |

The first four are implemented directly in the local chat boundary. The unavailable-backend response is the contract for wrapping a production vector client exception at the API boundary.