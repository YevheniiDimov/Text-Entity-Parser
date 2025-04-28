# Text-Entity-Parser

**Text-Entity-Parser** is a Python-based tool designed to parse natural language text into a hierarchical tree structure of entities and their associated features. This facilitates structured analysis and processing of unstructured textual data.

## Features

- **Hierarchical Parsing**: Converts plain text into a tree of entities and features.
- **Docker Support**: Includes Docker configurations for easy deployment.
- **API Endpoint**: Provides a `/tree` endpoint that accepts a `text` parameter and returns a JSON representation of the parsed structure.

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) installed on your system.

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/YevheniiDimov/Text-Entity-Parser.git
   cd Text-Entity-Parser
   ```

2. **Load the Docker image**:

   Extract the `algorithm.7z` archive to obtain `algorithm.tar`, then run:

   ```bash
   docker load < algorithm.tar
   ```

3. **Verify the Docker image**:

   ```bash
   docker images
   ```

4. **Start the application using Docker Compose**:

   ```bash
   docker-compose up
   ```

## Usage

Once the application is running, you can access the parsing functionality via the `/tree` endpoint.

### Example Request

```http
GET /tree?text=Your%20input%20text%20here
```

### Example Response

```json
{
  "entity": "RootEntity",
  "features": [
    {
      "entity": "SubEntity1",
      "features": []
    },
    {
      "entity": "SubEntity2",
      "features": [
        {
          "entity": "NestedEntity",
          "features": []
        }
      ]
    }
  ]
}
```

## Project Structure

- `app.py`: Main application file.
- `algorithm.py`: Contains the parsing logic.
- `node.py`: Defines the tree node structure.
- `Dockerfile`: Docker image configuration.
- `docker-compose.yml`: Docker Compose setup.
- `requirements.txt`: Python dependencies.

## License

This project is licensed under the MIT License.

