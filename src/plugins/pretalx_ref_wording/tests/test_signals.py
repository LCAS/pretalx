from pretalx_ref_wording.signals import register_ref_wording_locale


def test_register_ref_wording_locale_returns_expected_locale():
    result = register_ref_wording_locale(sender=None)
    assert result == [("en-rex", "English (REF Outputs)")]
