# SAGSBench Frontend

A deploy-ready static landing page and product preview for **SAGSBench by SafeAlign AI**.

## Run locally

```bash
cd frontend
python3 -m http.server 5173
```

Open `http://localhost:5173`.

## Deploy with GitHub Pages

This frontend is static HTML/CSS/JS and can be served from `/frontend` or copied into a `gh-pages` branch.

The repo includes `.github/workflows/pages.yml` to publish `/frontend` to GitHub Pages when enabled in the repository settings.
