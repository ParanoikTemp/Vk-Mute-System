import json
from vkbottle.user import User, Message
from vkbottle.dispatch.rules.base import ReplyMessageRule
from vkbottle.dispatch.middlewares import BaseMiddleware

from tokens import token

with open("data.json", encoding="utf-8") as f:
    data = json.load(f)
    user_ids = data["user_ids"]


class MuteSystem(BaseMiddleware[Message]):
    async def pre(self) -> None:
        if self.event.from_id in user_ids and self.event.from_id != 774177099:
            await user.api.messages.delete(cmids=str(self.event.conversation_message_id), peer_id=self.event.peer_id,
                                           delete_for_all=False)
            self.stop()


user = User(token=token)
user.labeler.vbml_ignore_case = True
user.labeler.message_view.register_middleware(MuteSystem)


def save():
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f)


async def edit(message, text):
    await user.api.messages.edit(peer_id=message.peer_id,
                                 message=text,
                                 conversation_message_id=message.conversation_message_id,
                                 keep_forward_messages=True)


@user.on.message(text="!мут <user_word>")
async def mute_user1(message: Message, user_word: str):
    if message.from_id == 774177099:
        user_id = int(user_word.split('|')[0][3:])
        if user_id not in user_ids:
            user_ids.append(user_id)
            save()
            await edit(message, message.text + "(&#10004;)")
        else:
            await edit(message, message.text + "(&#10060;)")


@user.on.message(text="!мут <user_word>")
async def mute_user1(message: Message, user_word: str):
    if message.from_id == 774177099:
        user_id = int(user_word.split('|')[0][3:])
        if user_id not in user_ids:
            user_ids.append(user_id)
            save()
            await edit(message, message.text + "(&#10004;)")
        else:
            await edit(message, message.text + "(&#10060;)")


@user.on.message(ReplyMessageRule(), text="!мут")
async def mute_user2(message: Message):
    if message.from_id == 774177099:
        user_id = message.reply_message.from_id
        if user_id not in user_ids:
            user_ids.append(user_id)
            save()
            await edit(message, message.text + "(&#10004;)")
        else:
            await edit(message, message.text + "(&#10060;)")


@user.on.message(text=("!размут <user_word>", "!размут"))
async def unmute_user(message: Message, user_word: str = None):
    if user_word is None and message.reply_message:
        user_id = message.reply_message.from_id
    elif user_word:
        user_id = int(user_word.split('|')[0][3:])
    else:
        return
    if user_id in user_ids:
        user_ids.remove(user_id)
        save()
        await edit(message, message.text + "(&#10004;)")
    else:
        await edit(message, message.text + "(&#10060;)")


if __name__ == '__main__':
    user.run_forever()
