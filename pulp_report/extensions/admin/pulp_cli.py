import datetime
from pulp.client.extensions.decorator import priority

CONTEXT = None

@priority()
def initialize(context):
    """
    :type context: pulp.client.extensions.core.ClientContext
    """
    global CONTEXT
    CONTEXT = context

    report_section = context.cli.create_section('report', 'Report section')
    profilediff_command = report_section.create_command('profilediff', 'Generate reports', run_profilediff)
    profilediff_command.create_option('--name', 'Name of the user', required=True)
    profilediff_command.create_flag('--show-date', 'If specified, the date will be displayed')

def run_profilediff(**kwargs):
    CONTEXT.prompt.write('Hello %s' % kwargs['name'])
    if kwargs['show-date']:
        CONTEXT.prompt.write(datetime.datetime.now())
