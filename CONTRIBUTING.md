# Contributing to 3MF Tools

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Expected Behavior

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on what is best for the community
- Show empathy towards others

### Unacceptable Behavior

- Harassment, trolling, or derogatory comments
- Publishing others' private information
- Any conduct inappropriate in a professional setting

## How to Contribute

### Reporting Bugs

Before creating bug reports, check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected vs actual behavior**
- **System information** (OS, Python version)
- **Self-test output** (`python self_test.py`)

**Bug Report Template:**
```markdown
**Environment:**
- OS: macOS 15.1
- Python: 3.13.9
- 3MF Tools: main branch

**Description:**
Brief description of the issue

**Steps to Reproduce:**
1. Step one
2. Step two
3. See error

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happened

**Self-Test Output:**
```
paste output here
```

**Additional Context:**
Any other relevant information
```

### Suggesting Enhancements

Enhancement suggestions are welcome! Include:

- **Clear use case** - Why is this needed?
- **Proposed solution** - How should it work?
- **Alternatives considered** - What other options did you think about?
- **Implementation ideas** - Optional technical approach

### Pull Requests

We actively welcome pull requests for:

- Bug fixes
- Documentation improvements
- New features
- Performance improvements
- Additional examples
- Test coverage

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/3mf-tools.git
cd 3mf-tools
```

### 2. Create Development Environment

```bash
# Install dependencies
./install.sh

# Or manually:
python3.13 -m venv venv
source venv/bin/activate
pip install trimesh numpy scipy meshio networkx lxml pytest black flake8
```

### 3. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 4. Make Changes

Follow coding standards (see below)

### 5. Test Changes

```bash
# Run self-test
python self_test.py

# Run any new tests
pytest tests/
```

### 6. Commit Changes

```bash
git add .
git commit -m "feat: Add awesome new feature"
```

Use conventional commits:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Adding tests
- `refactor:` - Code refactoring
- `perf:` - Performance improvements

### 7. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Coding Standards

### Python Style

Follow [PEP 8](https://pep8.org/) with these specifics:

- **Line length:** 100 characters
- **Indentation:** 4 spaces
- **Quotes:** Double quotes for strings
- **Docstrings:** Google style

**Format code with Black:**
```bash
black *.py mcp_server/*.py examples/*.py
```

**Check with flake8:**
```bash
flake8 *.py mcp_server/*.py examples/*.py --max-line-length=100
```

### Example Code Style

```python
def process_mesh(mesh_path: str, output_path: str, scale: float = 1.0) -> dict:
    """
    Process and transform a mesh file.

    Args:
        mesh_path: Path to input mesh file
        output_path: Path to save processed mesh
        scale: Scale factor to apply (default: 1.0)

    Returns:
        Dictionary with status and output path

    Raises:
        FileNotFoundError: If mesh_path doesn't exist
        ValueError: If scale is <= 0
    """
    if scale <= 0:
        raise ValueError("Scale must be positive")

    import trimesh

    mesh = trimesh.load(mesh_path)
    mesh.apply_scale(scale)
    mesh.export(output_path)

    return {"status": "success", "path": output_path}
```

### MCP Tool Standards

All MCP tools must follow these principles:

1. **File-based operations** - No large data in responses
2. **Status messages only** - Return paths and codes
3. **Silent by default** - Only output errors
4. **Idempotent** - Safe to run multiple times
5. **Low token usage** - Minimal JSON responses

**Example MCP tool:**
```python
@staticmethod
def example_tool(input_path: str, output_path: str) -> dict:
    """Tool description"""
    try:
        # Process
        result = do_processing(input_path, output_path)
        return {"status": "success", "path": output_path}
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

### Documentation

- **All functions** need docstrings
- **Complex logic** needs inline comments
- **Examples** help users understand usage
- **Update README** if adding features

## Testing

### Running Tests

```bash
# Run self-test
python self_test.py

# Run pytest (if available)
pytest tests/ -v

# Test examples
./examples/repair_mesh.py test_cube.stl output.stl
./examples/boolean_ops.py --example
```

### Writing Tests

Create tests in `tests/` directory:

```python
# tests/test_mesh_operations.py
import pytest
from mcp_server.server import MeshTools

def test_mesh_load():
    """Test mesh loading"""
    result = MeshTools.load("test_cube.stl")
    assert result["status"] == "success"
    assert result["vertices"] > 0
    assert result["faces"] > 0

def test_mesh_load_invalid():
    """Test error handling"""
    result = MeshTools.load("nonexistent.stl")
    assert result["status"] == "error"
```

### Test Coverage

Aim for:
- **Core functionality:** 80%+ coverage
- **Error handling:** Test failure cases
- **Edge cases:** Empty meshes, invalid formats

## Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Self-test passes (`python self_test.py`)
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commits follow conventional format
- [ ] No merge conflicts with main

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
How was this tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-test passes
- [ ] Documentation updated
- [ ] Tests added/updated

## Related Issues
Closes #123
```

### Review Process

1. **Automated checks** run on all PRs
2. **Maintainer review** within 1-2 weeks
3. **Address feedback** if requested
4. **Approval and merge** by maintainer

### After Merge

- PR is merged to `main`
- Your contribution is acknowledged
- Changes appear in next release

## Areas for Contribution

### High Priority

- [ ] Complete CuraEngine integration
- [ ] Bambu Lab Cloud API integration
- [ ] Additional test coverage
- [ ] Performance optimizations
- [ ] Documentation improvements

### Good First Issues

- [ ] Add more examples
- [ ] Improve error messages
- [ ] Add type hints
- [ ] Fix typos in docs
- [ ] Add format support

### Feature Requests

- [ ] Docker container
- [ ] Web UI for MCP server
- [ ] Mesh analysis tools
- [ ] Batch processing CLI
- [ ] PyMeshLab integration

## Development Resources

- **API Documentation:** [docs/API.md](docs/API.md)
- **Examples:** [docs/EXAMPLES.md](docs/EXAMPLES.md)
- **Troubleshooting:** [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

## Questions?

- **General questions:** Open a [Discussion](https://github.com/winemarshal68/3mf-tools/discussions)
- **Bug reports:** [Issues](https://github.com/winemarshal68/3mf-tools/issues)
- **Feature requests:** [Issues](https://github.com/winemarshal68/3mf-tools/issues)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to 3MF Tools!** 🎉
