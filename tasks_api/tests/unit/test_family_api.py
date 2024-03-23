import re

import pytest

from tasks_api.invitation.invitation_api import create_random_invitation_code


@pytest.mark.parametrize("indexcode", range(25))
def test_create_random_invitation_code(indexcode):

    length_expected = 8
    code = create_random_invitation_code()

    assert len(code) == length_expected

    regex = "^[A-Z0-9]*$"

    assert re.match(regex, code), f"Test n°{indexcode} : {code} does not match"
