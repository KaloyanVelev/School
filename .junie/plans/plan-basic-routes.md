---
sessionId: session-260708-131630-1lty
---

# Requirements

### Overview & Goals
The goal is to implement the foundational API routes required to populate the "School" project database from scratch. Since the database is currently empty, we will focus on administrative entities (Schools, Classes, Subjects) and User Management/Enrollment.

### Scope
- **In Scope**:
    - Implementing RESTful endpoints for Schools, Classes, and Subjects.
    - Implementing User listing and Role management.
    - Implementing Student enrollment (linking users to classes).
    - Creating necessary Schemas, Managers, and Resources for these entities.
- **Out of Scope**:
    - Academic tracking (Grades, Remarks).
    - Operational data (Schedules).
    - Complex relationships (Parent-Student).
    - Frontend implementation.

### User Stories
- **As an Admin**, I want to create a school so that I can start building the system structure.
- **As a Director**, I want to create classes and subjects within my school so that students and teachers can be organized.
- **As an Admin**, I want to see all registered users and assign them roles (e.g., Director, Teacher) so the system is properly managed.
- **As a Director**, I want to enroll users as students into specific classes so their academic progress can be tracked.

# Technical Design

### Current Implementation
- **Models**: Comprehensive SQLAlchemy models exist for all school-related entities.
- **Auth**: Basic `register` and `login` routes are implemented in `UserRegisterResource` and `UserLogInResource`.
- **Infrastructure**: The project uses `Flask-RESTful` for resources, `Marshmallow` for schemas, and a "Manager" pattern for business logic.

### Proposed Routes (Phase 1: Foundation)

#### 1. Administrative Setup
These routes allow building the school hierarchy in an empty database.
- **Schools**: `/schools`
    - `POST`: Create a new school. (Admin)
    - `GET`: List schools. (Admin)
- **Classes**: `/classes`
    - `POST`: Create a class (requires `school_id`). (Admin, Director)
    - `GET`: List classes. (Admin, Director)
- **Subjects**: `/subjects`
    - `POST`: Create a subject (requires `school_id`). (Admin, Director)
    - `GET`: List subjects. (Admin, Director)

#### 2. User & Enrollment Management
These routes allow populating the system with people.
- **Users**: `/users`
    - `GET`: List all registered users. (Admin)
- **User Roles**: `/users/<id>/role`
    - `PUT`: Update a user's role (permission level). (Admin)
- **Enrollment**: `/students`
    - `POST`: Link a user to a class as a student. (Admin, Director)
    - `GET`: List students (optionally filter by class).

### Key Decisions
- **Role-Based Access**: Use the `permission_required` decorator. Initially, since the DB is empty, the first user (Admin) should be created via the `admin_registering.py` script or by allowing the first registration to be an admin (riskier).
- **Manager Pattern**: Each resource will have a corresponding Manager in `managers/` to handle logic and database interaction.
- **Marshmallow Schemas**: Request validation and response serialization will be handled by schemas in `schemas/`.

### Architecture Mapping
New routes should follow the established pattern:
1. **Schema**: Create Marshmallow schemas in `schemas/request/` and `schemas/response/`.
2. **Manager**: Implement business logic in new files within `managers/` (e.g., `managers/grade.py`).
3. **Resource**: Create Flask-RESTful resource classes in `resources/` (e.g., `resources/grade.py`).
4. **Route**: Register the resources in `resources/routes.py`.

### Route Table (Phase 1)

 Resource | Path | Methods | Permission | Purpose |
 :--- | :--- | :--- | :--- | :--- |
 **School** | `/schools` | POST, GET | ADMIN | Create/List Schools |
 **Class** | `/classes` | POST, GET | ADMIN, DIRECTOR | Create/List Classes |
 **Subject** | `/subjects` | POST, GET | ADMIN, DIRECTOR | Create/List Subjects |
 **User List**| `/users` | GET | ADMIN | See registered users |
 **User Role**| `/users/<id>/role` | PUT | ADMIN | Promote/Demote users |
 **Student** | `/students` | POST, GET | ADMIN, DIRECTOR | Enroll user in class |

# Delivery Steps

###   Step 1: Plan Administrative Routes (Schools, Classes, Subjects)
Identify and document the necessary RESTful routes for managing Schools, Classes, and Subjects.
- Propose `GET`, `POST`, `PUT`, `DELETE` endpoints for each entity.
- Define access control rules (e.g., Admin for Schools, Director for Classes).
- Map routes to the corresponding database models (`SchoolModel`, `SchoolClassModel`, `SchoolSubjectModel`).

###   Step 2: Plan Academic Routes (Students, Grades, Remarks)
Identify and document routes for managing student data and academic performance.
- Propose routes for student profiles, linking users to classes, and listing students by class.
- Define endpoints for Grade and Remark management.
- Specify that only Teachers should have access to creating Grades and Remarks.
- Map routes to `StudentModel`, `GradeModel`, and `RemarkModel`.

###   Step 3: Plan Supplemental Routes (Schedules, Relationships)
Identify and document routes for complex entities like Schedules and Parent-Student associations.
- Propose routes for viewing and editing class schedules.
- Define endpoints for linking Parents to Students in the system.
- Specify access rules for Directors and Admins.
- Map routes to `ScheduleModel` and `ParentStudentModel`.

###   Step 4: Plan User Management Routes
Identify and document routes for advanced user management beyond auth.
- Propose routes for user profile updates and role management.
- Define endpoints for listing users with filtering by role.
- Map routes to `UserModel`.