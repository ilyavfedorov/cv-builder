import unittest
import urllib.error

from scripts.cloud_job_market_refresh import rate_limit_delay


class RateLimitDelayTests(unittest.TestCase):
    def test_uses_retry_after_header(self):
        error = urllib.error.HTTPError(
            "https://api.openai.com/v1/responses",
            429,
            "Too Many Requests",
            {"Retry-After": "7.5"},
            None,
        )

        self.assertEqual(rate_limit_delay(error, "", 0), 8.5)

    def test_uses_delay_from_error_message(self):
        error = urllib.error.HTTPError(
            "https://api.openai.com/v1/responses",
            429,
            "Too Many Requests",
            {},
            None,
        )

        self.assertEqual(
            rate_limit_delay(error, "Please try again in 7.631s.", 0),
            8.631,
        )

    def test_caps_exponential_fallback(self):
        error = urllib.error.HTTPError(
            "https://api.openai.com/v1/responses",
            429,
            "Too Many Requests",
            {},
            None,
        )

        self.assertEqual(rate_limit_delay(error, "", 4), 60.0)


if __name__ == "__main__":
    unittest.main()
