from unittest import mock

import nexmo
import pytest
from hotline import injector
from hotline.telephony import verification
from tests.telephony import helpers


# TODO NZ: test both paths:
# - (default) one nexmo.clientwhere the event has a primary number
# - and one where it does not
# (future: do we want to allow adding members
# before an event has a primary number?)
@mock.patch("time.sleep", autospec=True)
def test_start_member_verification(sleep, database):
    client = mock.create_autospec(nexmo.Client, instance=True)

    client.application_id = "appid"
    client.send_message.return_value = {"messages": [{"error-text": ""}]}

    injector.set("nexmo.client", client)
    injector.set("secrets.virtual_number", "1234567890")

    event = helpers.create_event()
    member = helpers.add_unverfied_members(event)

    verification.start_member_verification(member)

    expected_msg = (
        f"You've been added as a member of the {member.event.name} event on conducthotline.com."
        " Reply with YES or OK to confirm."
    )

    client.send_message.assert_called_once_with(
        {"from": event.primary_number, "to": member.number, "text": expected_msg}
    )
