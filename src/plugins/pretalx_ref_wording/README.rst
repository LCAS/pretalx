pretalx-ref-wording
===================

A pretalx plugin that overrides the default wording used throughout the
CfP/review/scheduling process (e.g. "Proposal" -> "Output", "Speaker" ->
"Author") without changing any underlying workflow, permissions, or data
model. This is intended for use cases such as reviewing scientific outputs
for the UK Research Excellence Framework (REF) using pretalx's existing
submission/review machinery.

How it works
------------

This plugin registers an additional "locale" (``en-rex``) via pretalx's
``register_locales`` signal. This is not a real spoken language - it is a
variant of English with a custom translation catalog
(``locale/en_Rex/LC_MESSAGES/django.po``) that only overrides the specific
terms you want changed. Every other string falls back to standard English.

Installation
------------

1. Install this plugin into your pretalx environment, e.g.::

    pip install -e src/plugins/pretalx_ref_wording

2. Restart pretalx so the plugin and its locale are detected.
3. In your event's organiser settings, under "Languages", add
   "English (REF Outputs)" as an available/default content locale.

Customising the wording
------------------------

Edit ``pretalx_ref_wording/locale/en_Rex/LC_MESSAGES/django.po`` and add or
change ``msgid``/``msgstr`` pairs for any string you want to reword. Leave
``msgstr ""`` (or remove the entry) for anything you want to keep as
standard English wording. After editing, compile the catalog::

    django-admin compilemessages -l en_Rex

(run from ``src/plugins/pretalx_ref_wording/pretalx_ref_wording``, or point
``--locale`` appropriately for your install).

This plugin makes no changes to CfP steps, review workflows, permissions,
or states - only display strings.
