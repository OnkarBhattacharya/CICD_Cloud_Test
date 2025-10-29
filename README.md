# Cloud Testing Proof of Concept (PoC)

This repository demonstrates comprehensive testing strategies for cloud-based applications, showcasing various test types, patterns, and best practices for distributed systems.

## Architecture Overview

The PoC consists of:
- **Backend**: Flask-based REST API for user management (Python)
- **Frontend**: React-based user interface (JavaScript/JSX)
- **Database**: SQLite for simplicity (easily replaceable with cloud databases)
- **Testing Suite**: Comprehensive tests covering all layers

## Test Types Demonstrated

### 1. Unit Tests (`user-service/tests/test_user_unit.py`)
- Tests individual components in isolation
- Focuses on the User model functionality
- Fast execution, no external dependencies
- **Example**: Testing user creation, validation, and serialization

### 2. Integration Tests (`user-service/tests/test_user_integration.py`)
- Tests API endpoints with database interactions
- Uses in-memory SQLite for isolation
- Verifies complete request-response cycles
- **Example**: Testing CRUD operations through HTTP API

### 3. Contract Tests (`user-service/tests/test_user_contract.py`)
- Ensures API contracts are maintained
- Validates request/response structures
- Prevents breaking changes for API consumers
- **Example**: Verifying JSON schema compliance

### 4. Performance Tests (`user-service/tests/test_performance.py`)
- Measures response times and throughput
- Tests concurrent request handling
- Monitors memory usage and resource consumption
- **Example**: Load testing user creation endpoints

### 5. Frontend Tests (`frontend/src/__tests__/App.test.jsx`)
- Tests React components and user interactions
- Mocks API calls for isolation
- Validates UI behavior and state management
- **Example**: Testing form submission and error handling

### 6. End-to-End Tests (`e2e-tests/test_e2e.py`)
- Tests complete user workflows
- Uses Selenium WebDriver for browser automation
- Validates entire application stack
- **Example**: Testing user creation through the UI

## Test Strategy Patterns Implemented

### Test Pyramid
- **Base (Unit Tests)**: Numerous, fast, isolated tests
- **Middle (Integration Tests)**: Moderate number, testing component interactions
- **Top (E2E Tests)**: Few, comprehensive, full-stack tests

### Shift-Left Testing
- Tests are written alongside development
- Early feedback through automated CI/CD integration
- Quality gates at multiple stages

### Service Virtualization
- Mocked external dependencies in unit/integration tests
- Isolated testing environments
- Predictable test data and scenarios

## Environment Strategies

### Ephemeral Test Environments
- Docker Compose for reproducible environments
- Isolated test databases (in-memory SQLite)
- Containerized test execution

### Data Management
- Automated test data seeding
- Clean state for each test run
- Realistic test scenarios

## CI/CD Integration Features

### Quality Gates
- Unit tests must pass before integration tests
- Integration tests must pass before E2E tests
- Performance benchmarks as quality criteria

### Fast Feedback
- Parallel test execution where possible
- Fail-fast strategies for quick feedback
- Comprehensive test reporting

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker and Docker Compose
- pnpm (for frontend)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cloud-testing-poc
   ```

2. **Set up the backend (create venv and install deps)**
   ```bash
   cd user-service
   # Create the venv (Windows: prefer `py -3` if available)
   py -3 -m venv venv
   # or (if py launcher not available)
   python -m venv venv

   # Activate the venv (see Activation notes below) then:
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

# Activation notes (Windows / macOS / Linux)
- PowerShell (Windows)
  ```powershell
  # Allow activation for this session if needed:
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
  .\venv\Scripts\Activate.ps1
  ```
- Command Prompt (Windows)
  ```cmd
  venv\Scripts\activate
  ```
- Git Bash (Windows)
  ```bash
  # Git Bash uses Unix-style paths but venv on Windows places scripts in Scripts/
  source venv/Scripts/activate
  ```
- WSL / macOS / Linux
  ```bash
  source venv/bin/activate
  ```

# Troubleshooting
- If "Python was not found" on Windows:
  - Install from https://www.python.org/downloads/windows and check "Add Python to PATH", or
  - Disable the Microsoft Store Python app execution aliases: Settings > Apps > Advanced app settings > App execution aliases (turn off "python" / "py"), then reopen the terminal.
- If commands like `python` are not recognized even after installing, use the venv interpreter explicitly:
  - Windows example: `.\venv\Scripts\python.exe <script>`
  - Or use the py launcher: `py -3 <script>`
- If you see "Could not open requirements file" — ensure you run the install command from the folder that contains requirements.txt (usually `user-service`), or give the correct relative path:
  ```powershell
  # from e2e-tests folder, install using the requirements in user-service
  py -3 -m pip install -r ..\user-service\requirements.txt
  ```

### Running Tests (backend)
```bash
cd user-service

# 1) Ensure the virtual environment exists:
py -3 -m venv venv  # preferred on Windows
# or
python -m venv venv

# 2) Activate the venv for your shell (PowerShell shown)
# PowerShell (Windows)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
.\venv\Scripts\Activate.ps1

# Command Prompt (Windows)
venv\Scripts\activate

# Git Bash (Windows)
source venv/Scripts/activate

# WSL / macOS / Linux
source venv/bin/activate

# 3) Install dependencies into the activated venv
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# If pytest is not present in requirements.txt:
python -m pip install pytest

# 4) Verify pytest is installed
# POSIX (bash / macOS / WSL):
python -m pip list | grep -i pytest || python -m pytest --version
# PowerShell:
python -m pip show pytest -ErrorAction SilentlyContinue
if ($LASTEXITCODE -ne 0) { python -m pytest --version }

# 5) Run tests
python -m pytest tests/test_user_unit.py -v
python -m pytest tests/test_user_integration.py -v
python -m pytest tests/test_user_contract.py -v
python -m pytest tests/test_performance.py -v
python -m pytest tests/ -v
```

### Common troubleshooting: "No module named pytest"
- Activate the venv in the same terminal where you run pytest.
- Confirm the active python executable:
  - PowerShell: `where.exe python`
  - macOS/Linux: `which python`
- Check installed packages: `python -m pip list`
- Install pytest into the active venv: `python -m pip install pytest`

### E2E Tests (requires running application)
```bash
# 1) Start the backend application (from user-service)
cd user-service
# Activate venv (PowerShell example)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
.\venv\Scripts\Activate.ps1

# Run the backend
python src/main.py
# or explicitly:
.\venv\Scripts\python.exe src/main.py

# 2) In another terminal run E2E tests
# Activate the same venv in the new terminal (PowerShell example)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
.\venv\Scripts\Activate.ps1

# Ensure E2E dependencies are installed (selenium, webdriver-manager)
python -m pip install selenium webdriver-manager

# From inside the e2e-tests folder (PowerShell)
```powershell
# Activate the venv for this session (if using a venv in user-service)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
..\user-service\venv\Scripts\Activate.ps1

```
# Run the test file from the current folder
```powershell
python test_e2e.py
# or, if 'python' is not recognized:
.\..\user-service\venv\Scripts\python.exe test_e2e.py
```

# From the repository root (PowerShell)
```powershell
# Activate the venv (user-service)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
.\user-service\venv\Scripts\Activate.ps1

# Run the test file by path from repo root
python e2e-tests\test_e2e.py
# or explicit venv interpreter
.\user-service\venv\Scripts\python.exe e2e-tests\test_e2e.py
```

Notes:
- Avoid using shell-specific operators like `|| true` or `grep` in PowerShell; README now shows cross-platform alternatives and PowerShell-safe commands.
- If a module (e.g. selenium) is missing: activate the venv and run `python -m pip install selenium webdriver-manager`.
- In VS Code, select the venv via "Python: Select Interpreter" so the integrated terminal and test runner use the same environment.


### Running with Docker Compose (from userßservice, i.e backend)
```bash
# start Docker Desktop app
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"

# Verify Docker availibility 
docker version
docker info
docker compose version

# Run all services and tests
docker-compose up --build

# Run specific test suites
docker-compose run test-runner
docker-compose run e2e-tests
```

## Test Execution Examples

### Unit Test Output
```
test_user_creation PASSED
test_user_repr PASSED
test_user_to_dict PASSED
test_user_validation PASSED
```

### Integration Test Output
```
test_get_empty_users PASSED
test_create_user PASSED
test_get_user_by_id PASSED
test_update_user PASSED
test_delete_user PASSED
```

### Performance Test Output
```
test_single_user_creation_performance PASSED (45.2ms)
test_bulk_user_creation_performance PASSED (2.1s for 50 users)
test_concurrent_user_creation_performance PASSED (1.8s for 10 concurrent)
```

## Key Testing Principles Demonstrated

### 1. Test Isolation
- Each test runs independently
- Clean state before each test
- No shared test data between tests

### 2. Test Reliability
- Deterministic test outcomes
- Proper error handling and timeouts
- Robust assertions and wait conditions

### 3. Test Maintainability
- Clear test naming and documentation
- Helper methods for common operations
- Separation of test data and test logic

### 4. Test Coverage
- Multiple test types for comprehensive coverage
- Critical path testing prioritized
- Edge cases and error conditions included

## Interoperability Features

### API Versioning
- RESTful API design with clear endpoints
- JSON request/response format
- HTTP status codes for different scenarios

### Error Handling
- Graceful degradation for network issues
- User-friendly error messages
- Proper HTTP error responses

### Cross-Origin Support
- CORS enabled for frontend-backend communication
- Flexible deployment configurations

## Monitoring and Observability

### Test Metrics
- Test execution times
- Test success/failure rates
- Performance benchmarks

### Application Metrics
- API response times
- Error rates
- Resource utilization

## Best Practices Implemented

1. **Test Naming**: Descriptive test names that explain the scenario
2. **Test Structure**: Arrange-Act-Assert pattern
3. **Test Data**: Realistic but minimal test data
4. **Test Documentation**: Clear comments and docstrings
5. **Test Organization**: Logical grouping by test type and functionality

## Extending the PoC

### Adding New Test Types
1. Create new test files following the naming convention
2. Implement tests using the established patterns
3. Update CI/CD configuration to include new tests

### Adding New Features
1. Implement feature with corresponding tests
2. Update API contracts if needed
3. Add E2E tests for new user workflows

### Scaling Considerations
1. Database migration from SQLite to cloud databases
2. Horizontal scaling of backend services
3. Load balancer configuration for high availability
4. Distributed testing across multiple environments

## Conclusion

This PoC demonstrates a comprehensive approach to testing cloud applications, covering all major test types and implementing industry best practices. It serves as a practical reference for building robust, reliable, and maintainable cloud-native applications with proper testing strategies.

