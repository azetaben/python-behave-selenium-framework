"""Setup configuration for the Behave Selenium Framework."""
from pathlib import Path
import importlib
import subprocess
import sys


def _load_setuptools():
    """Import setuptools and bootstrap it if the active environment is missing it."""
    try:
        setuptools_mod = importlib.import_module("setuptools")
        return setuptools_mod.setup, setuptools_mod.find_packages
    except ModuleNotFoundError:
        try:
            # Keep setup.py usable even in minimal virtual environments.
            subprocess.check_call([sys.executable, "-m", "pip", "install", "setuptools>=70"])
            setuptools_mod = importlib.import_module("setuptools")
            return setuptools_mod.setup, setuptools_mod.find_packages
        except Exception as exc:
            raise RuntimeError(
                "setuptools is required to run setup.py. "
                "Install it with: python -m pip install setuptools"
            ) from exc


def _read_requirements(requirements_path: Path) -> list[str]:
    """Load install requirements from requirements.txt (ignoring comments/blank lines)."""
    requirements: list[str] = []
    for raw_line in requirements_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        requirements.append(line)
    return requirements


ROOT = Path(__file__).resolve().parent
README = ROOT / "README.md"
REQUIREMENTS = ROOT / "requirements.txt"

setup, find_packages = _load_setuptools()

setup(
    name="python-behave-selenium-framework",
    version="1.0.0",
    description="Enterprise-grade test automation framework with Selenium 4 and Behave BDD",
    long_description=README.read_text(encoding="utf-8") if README.exists() else "",
    long_description_content_type="text/markdown",
    author="QA Automation Team",
    author_email="qa@example.com",
    url="https://github.com/azetaben/python-behave-selenium-framework.git",
    license="MIT",
    packages=find_packages(exclude=["tests", "features"]),
    python_requires=">=3.10",
    install_requires=_read_requirements(REQUIREMENTS) if REQUIREMENTS.exists() else [],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
    ],
    keywords="automation testing selenium python behave bdd",
)
