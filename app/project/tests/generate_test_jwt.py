from project.tests.base import BaseTestCase, generate_token_data, encode_token_date_with_hs256


class GenerateTestJWT(BaseTestCase):
    """
    Get a mocked JWT for testing.
    Note you have to change the
    """

    def test_echo_token(self):
        token_data = generate_token_data()
        hs256_token = encode_token_date_with_hs256(token_data)
        print("\n" + hs256_token + "\n")
