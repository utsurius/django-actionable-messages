from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="django_actionable_messages",
    packages=find_packages(exclude=["examples", "examples.*", "tests", "tests.*"]),
    include_package_data=True,
    version="0.2.7",
    license="MIT",
    description="Actionable messages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="utsurius",
    author_email="przemek@upsecure.pl",
    url="https://github.com/utsurius/django-actionable-messages",
    python_requires=">=3.6",
    keywords=["msteams", "AdaptiveCard", "MessageCard", "HeroCard", "ThumbnailCard", "actionable messages"],
    install_requires=[
        "django>=3.2.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    project_urls={
        "Documentation": "https://github.com/utsurius/django-actionable-messages/blob/master/README.md",
        "Source": "https://github.com/utsurius/django-actionable-messages",
        "Tracker": "https://github.com/utsurius/django-actionable-messages/issues",
    }
)
