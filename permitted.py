""" Copyright 2012, 2013 UW Information Technology, University of Washington

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from django.db.models import Q


class PermittedException(Exception): pass


class Permitted(object):
    def is_admin(self, user):
        if not (user.groups.filter(name='spacescout_admins').count() > 0):
            raise PermittedException('User not allowed to edit')

    def can_create(self, user):
        if not (user.groups.filter(Q(name='spacescout_admins') | Q(name='spacescout_creators')).count() > 0):
            raise PermittedException('User not allowed to edit')

    def can_edit(self, user, space, spot):
        if not (user.groups.filter(name='spacescout_admins').count() != 0
                or (user.is_authenticated()
                    and (user.username == space.manager)
                         or (user.username == spot.get('manager')))):
            raise PermittedException('User not allowed to edit')
