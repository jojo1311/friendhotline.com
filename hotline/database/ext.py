# Copyright 2019 Alethea Katherine Flowers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Flask extension for database stuff."""


from hotline.database import lowlevel


def _db_connect():
    lowlevel.db.connect()


def _db_close(response):
    if not lowlevel.db.is_closed():
        lowlevel.db.close()


def init_app(app):
    app.before_request(_db_connect)
    app.teardown_request(_db_close)
