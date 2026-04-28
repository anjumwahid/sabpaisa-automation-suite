FROM mcr.microsoft.com/playwright/python:v1.49.1-noble

WORKDIR /app

# Container has no display — force headless mode and disable slow-mo for CI speed.
# These can still be overridden at run time with `docker run -e HEADLESS=false ...`
ENV HEADLESS=true \
    SLOW_MO=0 \
    ENV=Staging

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["pytest", "tests/test_regression_suite.py", "--alluredir=reports/allure-results", "-v"]
