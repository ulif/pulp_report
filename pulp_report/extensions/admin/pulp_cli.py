# -*- coding: utf-8 -*-
from gettext import gettext as _
from pulp.client.extensions.decorator import priority
from pulp.client.extensions.extensions import PulpCliSection, PulpCliCommand


PROFILEDIFF_DESC = _("Show profile differences.")
SECT_DESC = _('create reports')


@priority()
def initialize(context):
    """
    :type context: pulp.client.extensions.core.ClientContext
    """
    report_section = ReportSection(context)
    context.cli.add_section(report_section)


class ReportSection(PulpCliSection):

    def __init__(self, context):
        """
        @param context:
        @type  context: pulp.client.extensions.core.ClientContext
        """
        PulpCliSection.__init__(self, 'report', SECT_DESC)
        self.context = context
        self.prompt = context.prompt  # for easier access

        self.add_command(ProfilediffReport(context))


class ProfilediffReport(PulpCliCommand):

    def __init__(self, context, name='profilediff',
                 description=PROFILEDIFF_DESC, method=None):
        self.context = context
        self.prompt = context.prompt

        if method is None:
            method = self.run

        super(ProfilediffReport, self).__init__(name, description, method)

        self.create_option('--master-id', 'Master consumer id', required=True)
        self.create_option(
            '--consumer-id', 'Consumer to compare to', required=False)
        self.create_option(
            '--group-id', 'Consumer group to compare to', required=False)

    def run(self, **kwargs):
        consumer_id = kwargs['consumer-id'] or kwargs['group-id']
        if (kwargs['consumer-id'] is not None) and (
                kwargs['group-id'] is not None):
            msg = _('These arguments cannot be used together')
            self.prompt.render_failure_message(msg)
            return
        # this chokes if `master-id` is not a valid consumer.
        self.context.server.consumer.consumer(id=kwargs['master-id'])
        consumer_ids = []
        if kwargs['consumer-id'] is not None:
            self.prompt.write(
                "* master <-> consumer '%s':" % kwargs['consumer-id'])
            # chokes if `consumer_id` is not a valid consumer.
            self.context.server.consumer.consumer(id=kwargs['consumer-id'])
            consumer_ids.append(kwargs['consumer-id'])
        elif kwargs['group-id'] is not None:
            self.prompt.write(
                "* master <-> consumer group '%s':" % kwargs['group-id'])
            group = self._get_group(kwargs['group-id'])
            if group is None:
                msg = _('Consumer Group not found: %s' % kwargs['group-id'])
                self.prompt.render_failure_message(msg)
                return
            consumer_ids.extend(group['consumer_ids'])
        else:
            msg = _('One of consumer-id or group-id is required.')
            self.prompt.render_failure_message(msg)
            return

        master_units = self._get_units(kwargs['master-id'])
        consumer_units = []
        for consumer_id in consumer_ids:
            consumer_units = self._get_units(consumer_id, consumer_units)

        changes = False
        for unit in master_units:
            if unit not in consumer_units:
                changes = True
                self.prompt.write("+ %s" % self._format_unit(unit))
        for unit in consumer_units:
            if unit not in master_units:
                changes = True
                self.prompt.write("- %s" % self._format_unit(unit))

        if not changes:
            self.prompt.write(_('No changes.'))

    def _format_unit(self, unit):
        """
        :param unit: A unit dict as contained in profiles
        :param
        """
        return "%s-%s-%s %s" % (
            unit['name'], unit.get('version', ''), unit.get('release', ''),
            unit.get('arch', ''))

    def _get_units(self, consumer_id, units_found=[]):
        """
        :param consumer_id: ID of a consumer
        :type  consumer_id: text

        :param units_found: list of already found units.
                            These will be skipped when found again.
        :type  units_found: list of dicts

        :return: List of "units" (normally: packages)
        :rtype: list of dicts
        """
        path = "/pulp/api/v2/consumers/%s/profiles/" % consumer_id
        profiles = self.context.server.consumer.server.GET(path).response_body
        for profile in profiles:
            for unit in profile.get('profile', []):
                if unit in units_found:
                    continue
                units_found.append(unit)
        return units_found

    def _get_group(self, group_id):
        """
        :param group_id: ID of a consumer group
        :type  group_id: text

        :return: consumer data if found, none else.
        :rtype:  dict or None
        """
        groups = self.context.server.consumer_group.consumer_groups(
            ).response_body
        for group in groups:
            if group.get('id', None) == group_id:
                return group
