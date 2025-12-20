# Contributing to Hornet Nest Locator

Thank you for your interest in contributing to the Hornet Nest Locator project! This tool helps protect honeybee populations by locating invasive Asian hornet nests.

## 🐝 Project Mission

Our mission is to provide beekeepers and conservationists with an accurate, scientifically-validated tool for locating Asian hornet nests to protect honeybee populations.

## 🤝 How to Contribute

We welcome contributions in several areas:

### 1. Bug Reports

If you find a bug, please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs. actual behavior
- Your environment (OS, Python version)
- Example data (if applicable)

### 2. Feature Requests

Have an idea? Open an issue describing:
- The feature and its benefits
- Use cases
- Proposed implementation (if you have ideas)

### 3. Code Contributions

#### Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/hornet-hive-locator.git
   cd hornet-hive-locator
   ```

2. **Set up development environment**
   ```bash
   # Install UV package manager
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Install dependencies
   uv sync
   ```

3. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

#### Development Guidelines

**Code Style:**
- We use `ruff` for linting and formatting
- Follow PEP 8 conventions
- Use type hints where possible

```bash
# Format code
uv run ruff format .

# Check for issues
uv run ruff check .

# Type checking
uv run mypy src/
```

**Testing:**
- Write tests for new features
- Ensure existing tests pass
- Aim for good test coverage

```bash
uv run pytest
```

**Documentation:**
- Update docstrings for new functions/classes
- Update README.md if adding user-facing features
- Add examples for new functionality

#### Pull Request Process

1. **Ensure quality**
   - All tests pass
   - Code is formatted with ruff
   - Type hints are added
   - Documentation is updated

2. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add wind compensation algorithm"
   ```
   
   Use conventional commit messages:
   - `feat:` - New features
   - `fix:` - Bug fixes
   - `docs:` - Documentation changes
   - `refactor:` - Code refactoring
   - `test:` - Test additions/changes
   - `chore:` - Build/tooling changes

3. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Open a Pull Request**
   - Describe what changed and why
   - Reference related issues
   - Include screenshots for UI changes
   - Wait for review

### 4. Documentation

Help improve documentation:
- Fix typos or unclear sections
- Add examples
- Translate documentation to other languages
- Create tutorials or guides

### 5. Field Testing & Feedback

As a beekeeper or conservationist:
- Test the app in real-world conditions
- Report accuracy of results
- Suggest improvements based on field experience
- Share success stories

## 🔬 Scientific Contributions

We especially welcome:

### Algorithm Improvements
- Wind compensation models
- Improved confidence calculations
- Alternative triangulation methods
- Machine learning approaches

### Data & Validation
- Field test data and results
- Comparison with professional tracking
- Regional behavior differences
- Species-specific adaptations

### Research Integration
- New scientific findings on hornet behavior
- Updated flight speed measurements
- Foraging pattern studies

## 📋 Areas for Contribution

Current needs (see Issues for details):

### High Priority
- [ ] Wind speed/direction compensation
- [ ] Mobile app (Android/iOS)
- [ ] Database for multi-session tracking
- [ ] Improved visualization options

### Medium Priority
- [ ] Export to KML/GPX formats
- [ ] Weather API integration
- [ ] Photo upload for marked hornets
- [ ] Statistics and analysis tools

### Nice to Have
- [ ] Multi-user collaboration mode
- [ ] Integration with wildlife databases
- [ ] Offline map support
- [ ] Voice recording for field notes

## 🧪 Testing Guidelines

### Unit Tests
- Test individual functions
- Mock external dependencies
- Cover edge cases

### Integration Tests
- Test component interactions
- Validate geographic calculations
- Test file I/O operations

### Field Tests
- Test with real observation data
- Validate against known nest locations
- Test in various conditions

## 📝 Code Review Process

All submissions require review:
1. Maintainer reviews code
2. Feedback is provided
3. You make requested changes
4. Once approved, PR is merged

**What we look for:**
- Code quality and clarity
- Test coverage
- Documentation completeness
- Adherence to project style
- Backward compatibility

## 🌍 Translation Contributions

Help make this tool accessible worldwide:

**Needed translations:**
- Spanish (España, América Latina)
- German (Deutschland, Schweiz, Österreich)
- Italian (Italia)
- Portuguese (Portugal, Brasil)
- Dutch (Nederland)
- Polish (Polska)

**Translation guidelines:**
- Translate README.md → README_XX.md (e.g., README_ES.md)
- Translate user-facing strings in main.py
- Consider regional terminology differences
- Maintain technical accuracy

## ⚠️ Important Considerations

### Safety First
- Never encourage unsafe nest approaches
- Always recommend professional removal
- Include appropriate warnings

### Scientific Accuracy
- Cite sources for algorithms
- Validate against research
- Document assumptions
- Note limitations clearly

### Conservation Focus
- Priority: Protect honeybees
- Respect local wildlife
- Consider ecological impact
- Promote responsible usage

## 🔐 Security

If you discover a security vulnerability:
1. **Do NOT** open a public issue
2. Email the maintainers directly
3. Allow time for a fix before disclosure

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be:
- Listed in project acknowledgments
- Credited in release notes
- Thanked in documentation

## 💬 Communication

- **Issues**: Bug reports, feature requests
- **Discussions**: General questions, ideas
- **Pull Requests**: Code contributions

## 📚 Resources

### Learn About Asian Hornets
- [Vespawatch.be](https://vespawatch.be)
- [PLOS ONE - Flight capacities study](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0198597)
- [Vespawatchers methodology](https://www.vespavelutina.co.uk/)

### Development Tools
- [UV Documentation](https://docs.astral.sh/uv/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

## ❓ Questions?

- Open a Discussion for general questions
- Check existing Issues for similar problems
- Review documentation first

---

**Thank you for helping protect the bees! 🐝**

Every contribution, no matter how small, helps conservationists and beekeepers combat invasive Asian hornet populations.
