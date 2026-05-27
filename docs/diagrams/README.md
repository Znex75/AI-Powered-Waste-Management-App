# EcoCycle System Diagrams

These diagrams describe the implemented waste-management application.

- `er-diagram.svg` maps the persisted Prisma/SQLite entities: `User`, `Scan`, `Listing`, and `Transaction`. Authentication and AI classification are shown as connected external services.
- `use-case-diagram.svg` describes user and administrator actions in the application.
- `dfd-context-diagram.svg` is the Level 0 context data flow diagram.
- `dfd-level-1-diagram.svg` expands the context process into core application processes and database stores.
- `index.html` presents all four diagrams in a print-friendly page.

Implementation references used:

- `backend/prisma/schema.prisma`
- `backend/routes/scans.js`
- `backend/routes/market.js`
- `backend/routes/user.js`
- `backend/routes/admin.js`
- `android/app/src/main/assets/scan.html`
- `android/app/src/main/assets/admin.html`
