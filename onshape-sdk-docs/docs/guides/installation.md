---
sidebar_position: 1
title: Installation
---

# Installation

## Install Package

```bash
pip install onshape-sdk-zachsharma
```

This installs the published package and its dependencies, including `requests` and `python-dotenv`.

## Project Structure

Your project can stay minimal:

```
my_project/
├── .env
└── your_script.py
```

## Environment Variables

Create a `.env` file in your project root with your Onshape API keys:

```env
ONSHAPE_ACCESS_KEY=your_access_key_here
ONSHAPE_SECRET_KEY=your_secret_key_here
```

:::tip Getting API Keys
Generate API keys at [https://dev-portal.onshape.com/keys](https://dev-portal.onshape.com/keys). You need a free or paid Onshape account.
:::

## Verify Installation

```python
from onshape_sdk import OnshapeClient

client = OnshapeClient.from_env()
result = client.test_auth()
print(result)  # Prints user info and document count
```
