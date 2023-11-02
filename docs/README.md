# VSCUBING api documentation

Documentation of vscubing api

### Accounts related

Endpoints for auth and user managing users

* [Sign up or Login via google](accounts/google/login/post.md) : `POST /accounts/google/login/`
* [Refresh token](accounts/token/refresh/post.md) : `POST /accounts/token/refresh/`

### Contests related

Endpoints for all contests logic on the website

* [Show contest results](contests/contest/contest_number/discipline/get.md) : `GET /contests/contest/:contest_number/:discipline/`
* [Show dashboard data](contests/dashboard/get.md) : `GET /api/contests/dashboard/`
* [Show leaderboard data](contests/leaderboard/discipline/get.md) : `GET /api/contests/leaderboard/<str:discipline>/`
* [Show ongoing contest](contests/ongoing_contest_number/get.md) : `GET /api/contests/ongoing_contest_number/`
* [Show scrambles/solves to solve](contests/solve_contest/contest_number/discipline/get.md) : `GET /api/contests/solve_contest/:contest_number/:discipline/`
* [Create solve](contests/solve_contest/contest_number/discipline/post.md) : `POST /api/contests/solve_contest/:contest_number/:discipline/`
* [Update solve](contests/solve_contest/contest_number/discipline/put.md) : `PUT /api/contests/solve_contest/:contest_number/:discipline/`
* [Show solve reconstruction and details](contests/solve_reconstruction/get.md) : `GET /api/contests/solve_reconstruction/:id/`

#### In development, not supposed to work
* [Show leaderboard](contests/leaderboard/discipline/get.md) : `GET /api/contests/leaderboard/:discipline/`

### Contest related