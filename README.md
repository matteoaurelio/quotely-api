# Quotely API

This is a simple FastAPI-based service that generates downloadable CSV files from quotes. It is designed to be used with a custom GPT assistant to extract meaningful quotes for social media or publishing.

## Endpoint

- **POST /generate-csv**: Accepts a list of quotes and returns a downloadable CSV file.
- Protected by an optional API token in the header (`x-api-token`).

## Example Payload

```json
{
  "quotes": [
    {
      "quote": "You may not control all the events...",
      "strategy_used": "theme_based",
      "presentation_style": "maya_angelou",
      "source_page": 87
    }
  ]
}
