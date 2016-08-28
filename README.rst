pulp_report
===========

Support for reports for `Pulp <https://pulpproject.org>`_ Platform.

This extension provides a new ``report`` section for the `pulp-admin`
client::

  $ pulp-admin report --help
  Usage: pulp-admin [SUB_SECTION, ..] COMMAND
  Description: create reports

  Available Commands:
    profilediff - Show profile differences.


We provide the following commands:

- `profilediff`::

    $ pulp-admin report profilediff --help
    Command: profilediff
    Description: Show profile differences.

    Available Arguments:

      --master-id   - (required) Master consumer id
      --consumer-id - Consumer to compare to
      --group-id    - Consumer group to compare to

This report lists the differences between the profile of a master (a
`pulp` consumer) and another consumer (or a group thereof).
