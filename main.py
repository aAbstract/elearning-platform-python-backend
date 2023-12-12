import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import lib.log as log_man
import lib.http_response as http_resp_man

# normal routes
from routes import auth_api
from routes import payment_api
from routes import lectures_api
from routes import user_api
from routes import announcements_api

# admin routes
from routes.admin import coupons_api as admin_coupons_api
from routes.admin import users_api as admin_users_api
from routes.admin import dev_api as admin_dev_api
from routes.admin import lectures_api as admin_lectures_api
from routes.admin import materials_api as admin_materials_api
from routes.admin import payment_logs_api as admin_payment_logs_api
from routes.admin import stats_api as admin_stats_api
from routes.admin import announcements_api as admin_announcements_api


server = FastAPI()

# middle wares
server.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

# register routes
# normal routes
server.include_router(auth_api.router)
server.include_router(payment_api.router)
server.include_router(lectures_api.router)
server.include_router(user_api.router)
server.include_router(announcements_api.router)

# admin routes
server.include_router(admin_coupons_api.router)
server.include_router(admin_users_api.router)
server.include_router(admin_dev_api.router)
server.include_router(admin_lectures_api.router)
server.include_router(admin_materials_api.router)
server.include_router(admin_payment_logs_api.router)
server.include_router(admin_stats_api.router)
server.include_router(admin_announcements_api.router)


@server.get('/api/test')
async def test_get():
    log_man.add_log('main.test_get', 'DEBUG', 'hit test get route')
    return http_resp_man.create_json_response(msg='server online')

# mount static files server
server.mount("/", StaticFiles(directory="public",
             html=True), name="public")

if __name__ == '__main__':
    uvicorn.run(server, host='0.0.0.0', port=8080)
