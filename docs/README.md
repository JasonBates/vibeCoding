# Documentation Index

This directory contains comprehensive documentation for the VibeCoding Haiku Generator project.

## 📚 Available Documentation

### Core Documentation
- **[Main README](../README.md)** - Project overview, setup, and quick start guide
- **[Architecture](ARCHITECTURE.md)** - Detailed architecture patterns, design decisions, and implementation approaches
- **[Branch Review](BRANCH_REVIEW.md)** - Complete feature review and merge readiness assessment

### Development & CI/CD
- **[GitHub Actions Update](GITHUB_ACTIONS_UPDATE.md)** - GitHub Actions workflow configuration and testing setup
- **[Integration Tests](../tests/integration/README.md)** - Integration testing documentation

## 🏗️ Architecture Overview

The project follows modern Python architecture patterns:

- **Repository Pattern** - Clean data access layer
- **Service Layer** - Business logic encapsulation
- **Data Models** - Type-safe dataclasses with serialization
- **Graceful Degradation** - Works with/without external services

## 🧪 Testing Strategy

- **Unit Tests** - Fast, isolated component testing
- **Integration Tests** - Real API and database testing
- **Pre-commit Hooks** - Code quality enforcement
- **CI/CD Pipeline** - Automated testing and deployment

## 🚀 Quick Links

- [Setup Instructions](../README.md#setup)
- [Architecture Details](ARCHITECTURE.md)
- [Running Tests](../README.md#testing)
- [GitHub Actions](GITHUB_ACTIONS_UPDATE.md)

## 📝 Contributing

When adding new features or making changes:

1. Update relevant documentation
2. Add tests for new functionality
3. Update architecture docs if patterns change
4. Ensure all tests pass before submitting PR

---

*This documentation is maintained alongside the codebase and should be updated when making significant changes.*
