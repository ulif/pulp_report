import datetime
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

        self.create_option('--name', 'Name of the user', required=True)
        self.create_flag('--show-date', 'If specified, the date will be displayed')


    def run(self, **kwargs):
        self.prompt.write('Hello %s' % kwargs['name'])
        if kwargs['show-date']:
            self.prompt.write(datetime.datetime.now())
