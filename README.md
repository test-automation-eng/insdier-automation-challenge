# Insider Automation Challenge

This repository contains **UI automation**, **API automation**, and **basic load testing**
implemented using **Python**, **Pytest**, **Selenium**, and **Locust**.

The goal of this project is to demonstrate a practical automation framework
covering different test layers.

---

## Tech Stack
- Python 3
- Pytest
- Selenium WebDriver
- Requests (API testing)
- Allure (reporting)
- Locust (load testing)

---

## Project Structure

```text

├── api_tests/         # API automation (Petstore CRUD tests)
├── test/              # UI tests
├── pages/             # Page Object Model (POM)
├── load/              # Locust load test scripts
├── conftest.py        # Pytest fixtures and browser setup
├── pytest.ini         # Pytest configuration
├── requirements.txt   # Project dependencies
└── README.md
```

##  Setup

### 1. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate

- Install dependencies
pip install -r requirements.txt

- UI Tests (Selenium + Pytest)
Run all UI tests (Chrome by default)
pytest test/

- Run with Firefox
pytest test/ --browser=firefox

- Run in headless mode
pytest test/ --browser=chrome --headless
```
---
##  Allure Report 
```bash
- Generate results
pytest --alluredir=allure-results

- View report
allure serve allure-results
```
---
### Load Testing (Locust)
- Run Locust :
locust -f load/locustfile.py


- Open browser at:
http://localhost:8089
---


