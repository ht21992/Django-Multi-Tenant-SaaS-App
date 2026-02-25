# Django Multi-Tenant SaaS App

A multi-tenant SaaS application built with Django and PostgreSQL using schema-based isolation via django-tenants

Each tenant has its own PostgreSQL schema while sharing the same database

## Features

- Schema-based multi-tenancy
- Separate database schema per tenant
- Public and tenant-specific apps
- Tenant-based admin panel
- django-allauth authentication
- HTMX integration
- Automatic schema switching via middleware
- Subdomain-based tenant routing

### How It Works

- public schema → shared apps (tenants management, auth, etc.)

- Tenant schemas → isolated data per tenant

- Middleware detects subdomain and switches schema automatically

| URL                         | Schema Used |
| --------------------------- | ----------- |
| `localhost:8000`            | public      |
| `coffeeshop.localhost:8000` | coffeeshop  |

## Installation

1. Clone the repository:

```bash
git clone https://github.com/ht21992/Django-MultiTenant.git
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure Environment Variables:

```bash
SECRET_KEY=your-secret-key
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
```

5. Configure PostgreSQL:

```bash
CREATE DATABASE postgres;
```

6. Run Migrations (Public Schema):

```bash
python manage.py migrate_schemas --shared
```

7. Creating a Tenant

```bash
python manage.py create_tenant
```

Example

schema_name: coffeeshop
name: Coffee Shop
domain: coffeeshop.localhost

8. Create Tenant Superuser

```bash
python manage.py create_tenant_superuser
```

6. Start the development server:

```bash
python manage.py runserver
```

Access:

Public:
http://localhost:8000

Tenant:
http://coffeeshop.localhost:8000

### 🛠 Useful Commands

#### Migrate all schemas:

```bash
python manage.py migrate_schemas
```

#### Migrate specific tenant:

```bash
python manage.py migrate_schemas --schema=coffeeshop
```

### Connect to shell

```bash
python manage.py tenant_command shell --schema=coffeeshop
```

#### Create tenant:

```bash
python manage.py create_tenant
```

#### Create tenant superuser:

```bash
python manage.py create_tenant_superuser
```

## License

MIT License
