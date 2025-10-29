# Azure DevOps CI/CD Demo

This project demonstrates the integration of Continuous Integration and Continuous Delivery (CI/CD) practices using Azure DevOps for a cloud-native application built with TypeScript and Express.

## Project Structure

```
azure-devops-cicd-demo
├── src
│   ├── app.ts                # Entry point of the application
│   ├── controllers           # Contains route controllers
│   │   └── index.ts          # Index controller for handling routes
│   ├── services              # Contains business logic
│   │   └── index.ts          # Service class for business logic
│   └── types                 # Type definitions
│       └── index.ts          # Request and response interfaces
├── test
│   ├── unit                  # Unit tests
│   │   └── app.spec.ts       # Unit tests for app.ts
│   └── integration           # Integration tests
│       └── integration.spec.ts # Integration tests for component interactions
├── infra
│   ├── kubernetes            # Kubernetes configurations
│   │   ├── deployment.yaml    # Deployment configuration
│   │   ├── service.yaml       # Service configuration
│   │   └── ingress.yaml       # Ingress configuration
│   └── helm                  # Helm chart configurations
│       ├── Chart.yaml         # Helm chart metadata
│       └── values.yaml        # Helm chart values
├── .azure-pipelines           # Azure Pipelines configurations
│   ├── azure-pipelines.yml     # Main CI/CD pipeline configuration
│   └── templates              # Pipeline templates
│       ├── pr.yml            # Pull request pipeline template
│       ├── build.yml         # Build pipeline template
│       └── deploy.yml        # Deployment pipeline template
├── Dockerfile                 # Docker image build instructions
├── .gitignore                 # Git ignore file
├── package.json               # npm configuration file
├── tsconfig.json             # TypeScript configuration file
├── jest.config.js            # Jest configuration file
└── README.md                 # Project documentation
```

## Getting Started

### Prerequisites

- Node.js and npm installed
- Docker installed
- Access to Azure DevOps

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd azure-devops-cicd-demo
   ```

2. Install dependencies:
   ```
   npm install
   ```

### Running the Application

To run the application locally, use the following command:
```
npm start
```

### Running Tests

To run unit tests, use:
```
npm test
```

### CI/CD Pipeline

This project is configured with Azure DevOps for CI/CD. The pipeline includes stages for building, testing, and deploying the application. 

- **Build Stage:** Compiles the application and runs unit tests.
- **Test Stage:** Executes integration tests.
- **Deploy Stage:** Deploys the application to a Kubernetes cluster.

### Deployment

The application can be deployed using Helm charts defined in the `infra/helm` directory. Ensure that your Kubernetes cluster is set up and accessible.

### Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

### License

This project is licensed under the MIT License. See the LICENSE file for details.