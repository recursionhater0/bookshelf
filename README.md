# Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Installation
### 1. Clone the Repository

```bash
git clone git@github.com:recursionhater0/bookshelf.git
```
### 2. Build and Run with Docker

Use the Makefile commands to build and start the application:

```bash
make build
make up
```
Access the Application. The application should now be running at http://localhost:8000.

## Further improvements
1. Add poetry
2. Multistage building in Docker
3. Fixed dependency hell (watch requirements.txt). Split then into dev and prod envs.
4. Add tests