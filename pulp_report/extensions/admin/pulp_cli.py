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

    def __init__(self, context, name='profilediff', description=PROFILEDIFF_DESC, method=None):
        self.context = context
        self.prompt = context.prompt

        if method is None:
            method = self.run

        super(ProfilediffReport, self).__init__(name, description, method)

        self.create_option('--master-id', 'Master consumer id', required=True)
        self.create_option('--consumer-id', 'Consumer to compare to', required=False)
        self.create_option('--group-id', 'Consumer group to compare to', required=False)

    def run(self, **kwargs):
        consumer_id = kwargs['consumer-id'] or kwargs['group-id']
        if (kwargs['consumer-id'] is not None) and (kwargs['group-id'] is not None):
            msg = _('These arguments cannot be used together')
            self.prompt.render_failure_message(msg)
            return
        if consumer_id is None:
            msg = _('One of consumer-id or group-id must be given.')
            self.prompt.render_failure_message(msg)
            return

        self.prompt.write("* master <-> consumer '%s':" % kwargs['consumer-id'])
