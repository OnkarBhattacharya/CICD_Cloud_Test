# Azure DevOps CI/CD Demo

This project demonstrates the integration of Continuous Integration and Continuous Delivery (CI/CD) practices using Azure DevOps for a cloud-native application built with TypeScript and Express.

## Project Structure

```
azure-devops-cicd-demo
├── src
│   ├── app.ts                # Express application entry point
│   ├── controllers           # Contains route controllers
│   │   └── index.ts         # Index controller with welcome endpoint
│   ├── services             # Business logic services
│   └── types                # TypeScript type definitions
├── test
│   ├── unit                 # Unit tests
│   │   └── app.spec.ts      # Tests for main application
│   └── integration          # Integration tests
│       └── integration.spec.ts # API endpoint tests
├── dist                     # Compiled JavaScript output
├── package.json             # Project dependencies and scripts
├── tsconfig.json           # TypeScript configuration
└── README.md               # Project documentation
```

## Getting Started

### Prerequisites

- Node.js 18+ and npm installed
- TypeScript installed globally (`npm install -g typescript`)
- Git for version control

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd azure-devops-cicd-demo
```

2. Install dependencies:
```bash
npm install
```

### Development

Build the TypeScript code:
```bash
npm run build
```

Start the application:
```bash
npm start
```

The application will be available at `http://localhost:3000`

### Running Tests

Run all tests:
```bash
npm test
```

Run specific test suites:
```bash
npm run test:unit        # Unit tests only
npm run test:integration # Integration tests only
```

### API Endpoints

- `GET /`: Returns welcome message
  - Response: `{ "message": "Welcome to the CI/CD Demo Application!" }`

### Project Configuration

- **TypeScript Configuration** (`tsconfig.json`):
  - Targets ES6
  - Uses CommonJS modules
  - Outputs to `./dist` directory
  - Includes both source and test files

- **Package Scripts**:
  - `build`: Compiles TypeScript to JavaScript
  - `start`: Runs the compiled application
  - `test`: Runs all tests
  - `test:unit`: Runs unit tests
  - `test:integration`: Runs integration tests

### Contributing

1. Create a feature branch
2. Make your changes
3. Run tests to ensure everything works
4. Submit a pull request

### License

This project is licensed under the MIT License.