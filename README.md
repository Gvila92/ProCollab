
### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\

### `npm run build`



The Task Manager App is a web application built with a Flask API backend and a React frontend. It allows users to manage tasks, comments, and tags in a collaborative environment.

Features
User Management:

Create and view users.
Ensure usernames contain only letters.
Task Management:

Full CRUD operations for tasks.
Title and description are required.
Tasks are associated with users.
Comment System:

Create and view comments for tasks.
Tagging System:

Create and view tags for tasks.
Many-to-many relationship between tasks and tags.
Data Validation:

Validate task and user IDs to be integers.
Validate usernames to contain only letters.
React Frontend:

Utilizes React for a dynamic and responsive user interface.
Client-side routing with React Router.
API Endpoints
/api/users: User management.
/api/tasks: Task management.
/api/comments: Comment system.
/api/tasktags: Tagging system.
