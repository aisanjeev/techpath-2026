# API-First Design with OpenAPI

**Module 16 -- Spec-Kit Development Methodology | Topic 4**

---

## What is API-First Design?

API-First design means you write the API specification before you write any code. You define every endpoint, every request body, every response shape, and every error code in a document -- and only then do you start coding.

Think of it like a restaurant kitchen. Before the chef starts cooking, the restaurant prints a menu. The menu is a contract with the customer: "If you order butter chicken, you will get butter chicken -- not dal makhani." The API spec is that menu. It tells the frontend team exactly what they can order from the backend and what they will get back.

---

## Why Write the Contract Before Code?

Without an API spec, frontend and backend teams run into constant problems:

| Problem | Without API Spec | With API Spec |
|---------|-----------------|---------------|
| Field naming | Frontend expects `user_name`, backend sends `username` | Both agree on `username` upfront |
| Response format | Frontend expects an array, backend sends an object | Shape is documented and agreed |
| Missing endpoints | Frontend needs an endpoint that does not exist yet | All endpoints listed before coding |
| Error handling | Frontend does not know what error codes to expect | Error responses documented |
| Parallel work | Frontend waits for backend to finish | Both teams work simultaneously |

API-First design enables **parallel development**. The frontend team can build against mock data that matches the spec. The backend team builds the real implementation. When both are done, they connect -- and it works because both followed the same contract.

---

## OpenAPI 3.0: The Industry Standard

OpenAPI (formerly known as Swagger) is the most widely used format for describing REST APIs. It is a YAML or JSON file that describes every aspect of your API.

### Structure of an OpenAPI Spec

An OpenAPI spec has these main sections:

```
openapi: 3.0.0       --> Version of the OpenAPI standard
info:                 --> Metadata about the API
paths:                --> All endpoints (routes)
components:           --> Reusable schemas, parameters, responses
tags:                 --> Grouping for endpoints
servers:              --> Base URLs for the API
```

---

## Writing Your First OpenAPI Spec

Let us build a spec for a simple Todo API that Vikram is creating for his productivity app.

### Basic Info and Server

```yaml
openapi: 3.0.0
info:
  title: Todo API
  description: A simple task management API for VikramTasks app
  version: 1.0.0
  contact:
    name: Vikram Patel
    email: vikram@techpath.biz

servers:
  - url: http://localhost:8000/api/v1
    description: Local development server
  - url: https://api.vikramtasks.in/api/v1
    description: Production server
```

### Defining Endpoints (Paths)

Each endpoint specifies the HTTP method, parameters, request body, and responses.

```yaml
paths:
  /todos:
    get:
      tags:
        - Todos
      summary: List all todos
      description: Returns a paginated list of todos for the authenticated user
      parameters:
        - name: skip
          in: query
          description: Number of items to skip
          required: false
          schema:
            type: integer
            default: 0
        - name: limit
          in: query
          description: Maximum number of items to return
          required: false
          schema:
            type: integer
            default: 20
            maximum: 100
        - name: status
          in: query
          description: Filter by completion status
          required: false
          schema:
            type: string
            enum: [pending, completed, all]
            default: all
      responses:
        '200':
          description: List of todos retrieved successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Todo'
                  timestamp:
                    type: string
                    format: date-time
          headers:
            X-Total-Count:
              description: Total number of todos
              schema:
                type: integer
        '401':
          $ref: '#/components/responses/Unauthorized'

    post:
      tags:
        - Todos
      summary: Create a new todo
      description: Creates a new todo item for the authenticated user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TodoCreate'
      responses:
        '201':
          description: Todo created successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  data:
                    $ref: '#/components/schemas/Todo'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'

  /todos/{todo_id}:
    get:
      tags:
        - Todos
      summary: Get a specific todo
      parameters:
        - name: todo_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Todo retrieved successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                  data:
                    $ref: '#/components/schemas/Todo'
        '404':
          $ref: '#/components/responses/NotFound'

    put:
      tags:
        - Todos
      summary: Update a todo
      parameters:
        - name: todo_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TodoUpdate'
      responses:
        '200':
          description: Todo updated successfully
        '404':
          $ref: '#/components/responses/NotFound'

    delete:
      tags:
        - Todos
      summary: Delete a todo
      parameters:
        - name: todo_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Todo deleted successfully
        '404':
          $ref: '#/components/responses/NotFound'
```

### Defining Reusable Schemas (Components)

Schemas define the shape of your data. Using `$ref` avoids repeating the same definition.

```yaml
components:
  schemas:
    Todo:
      type: object
      properties:
        id:
          type: integer
          example: 1
        title:
          type: string
          example: "Buy groceries from DMart"
        description:
          type: string
          example: "Rice 5kg, Toor Dal 2kg, Cooking Oil 1L"
        status:
          type: string
          enum: [pending, completed]
          example: "pending"
        priority:
          type: string
          enum: [low, medium, high]
          example: "medium"
        due_date:
          type: string
          format: date
          example: "2026-08-01"
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time
      required:
        - id
        - title
        - status
        - created_at

    TodoCreate:
      type: object
      properties:
        title:
          type: string
          minLength: 1
          maxLength: 200
          example: "Complete Module 16 assignment"
        description:
          type: string
          maxLength: 1000
        priority:
          type: string
          enum: [low, medium, high]
          default: medium
        due_date:
          type: string
          format: date
      required:
        - title

    TodoUpdate:
      type: object
      properties:
        title:
          type: string
          minLength: 1
          maxLength: 200
        description:
          type: string
          maxLength: 1000
        status:
          type: string
          enum: [pending, completed]
        priority:
          type: string
          enum: [low, medium, high]
        due_date:
          type: string
          format: date

  responses:
    BadRequest:
      description: Invalid request data
      content:
        application/json:
          schema:
            type: object
            properties:
              success:
                type: boolean
                example: false
              error:
                type: string
                example: "Validation error"
              details:
                type: array
                items:
                  type: object
                  properties:
                    field:
                      type: string
                    message:
                      type: string

    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            type: object
            properties:
              success:
                type: boolean
                example: false
              error:
                type: string
                example: "Authentication required"

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            type: object
            properties:
              success:
                type: boolean
                example: false
              error:
                type: string
                example: "Todo not found"
```

---

## Swagger UI: Interactive Documentation

Once you have an OpenAPI spec, tools like **Swagger UI** turn it into interactive documentation. Developers can:

- See all endpoints grouped by tags
- View request/response schemas with examples
- Try out API calls directly from the browser
- See error responses and status codes

FastAPI generates Swagger UI automatically at `/docs` when you define your endpoints with proper type hints and Pydantic models.

| Tool | What It Does | URL |
|------|-------------|-----|
| Swagger UI | Interactive API explorer | `/docs` (built into FastAPI) |
| ReDoc | Beautiful API documentation | `/redoc` (built into FastAPI) |
| Swagger Editor | Online YAML editor with live preview | editor.swagger.io |
| Stoplight Studio | Visual API design tool | Free desktop app |

---

## Generating Client SDKs

One powerful benefit of OpenAPI specs is **code generation**. From a single YAML file, you can auto-generate:

- Python client libraries
- TypeScript/JavaScript client code
- API documentation
- Server stubs
- Test cases

```bash
# Install the OpenAPI generator
npm install -g @openapitools/openapi-generator-cli

# Generate a Python client from your spec
openapi-generator-cli generate \
  -i api-spec.yaml \
  -g python \
  -o ./generated-client

# Generate a TypeScript client for the frontend
openapi-generator-cli generate \
  -i api-spec.yaml \
  -g typescript-axios \
  -o ./frontend/src/api
```

This means the frontend team gets type-safe API functions automatically. No more guessing field names or response shapes.

---

## Best Practices for API Specs

| Practice | Example | Why |
|----------|---------|-----|
| Use consistent naming | `snake_case` for fields | Prevents confusion between teams |
| Version your API | `/api/v1/todos` | Allows breaking changes in v2 without breaking v1 |
| Document all error codes | 400, 401, 403, 404, 500 | Frontend knows what to handle |
| Include examples | `example: "Buy groceries"` | Makes the spec self-explanatory |
| Use $ref for reuse | `$ref: '#/components/schemas/Todo'` | Avoids duplication, single source of truth |
| Add descriptions | Every field, parameter, endpoint | Helps new team members understand quickly |

---

## Key Takeaways

1. API-First means writing the API contract before writing code.
2. OpenAPI 3.0 is the industry standard for describing REST APIs.
3. The spec includes paths (endpoints), schemas (data shapes), and responses (status codes).
4. Swagger UI turns your spec into interactive, testable documentation.
5. Code generators can produce client libraries from a single spec file.
6. API-First enables frontend and backend teams to work in parallel.

---

*TechPath Institute -- Spec-Kit Development Methodology*
