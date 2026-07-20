"""Serviços públicos da ZapZapApi Python Client."""

from zapzapapi.services.account import AccountService
from zapzapapi.services.chats import ChatsService
from zapzapapi.services.contacts import ContactsService
from zapzapapi.services.groups import GroupsService
from zapzapapi.services.instances import InstancesService
from zapzapapi.services.messages import MessagesService
from zapzapapi.services.profile import ProfileService

__all__ = [
    "AccountService",
    "ChatsService",
    "ContactsService",
    "GroupsService",
    "InstancesService",
    "MessagesService",
    "ProfileService",
]
