from django.utils.translation import ugettext as _
from datetime import date
from jobs_manager_app.models import Notification


STATE = {
    0: {'state': _('Assignment created'), 'next': _('Price/ETA proposal'),
        'desc': ''},
    1: {'state': _('Offer proposed'), 'next': _('Confirmation'),
        'desc': ''},
    -1: {'state': _('Assignment rejected'),
         'next': _('Price/ETA reevaluation'), 'desc': ''},
    2: {'state': _('Assignment in progress'), 'next': _('Job done'),
        'desc': ''},
    -2: {'state': _('Assignment in hold'), 'next': _('Meeting/Conditions'),
         'desc': ''},
    3: {'state': _('Assignment completed'), 'next': _('Payment'),
        'desc': ''},
    -3: {'state': _('Payment in hold'), 'next': _('Payment'),
         'desc': ''},
    4: {'state': _('Assignment paid'), 'next': _('Closure'),
        'desc': ''},
    5: {'state': _('Assignment closed'), 'next': _('Nothing'),
        'desc': ''},
    }


def notif_new_task(task):
    title = (_('New task: %(task_name)s.')
             % {'task_name': task.name})
    body = _('When: %(date)s.\n\n'
             'Where:\n'
             'Project: %(project)s.\n'
             'Assignment: %(assign)s (Dev: %(dev)s).\n\n'
             '\033[1m New Task:\033[1m\n'
             'Name: %(task)s. Priority: %(priority)d.\n'
             'Description: %(description)s'
             ) % {'date': date.today(), 'project': task.assignment.project,
                  'assign': task.assignment, 'dev': task.assignment.dev,
                  'task': task, 'priority': task.priority,
                  'description': task.description}

    notif = Notification(name=title, description=body, int_type=0,
                         user=task.collaborator.email)
    return notif


def notif_new_assignment(assignment):
    title = (_('New assignment: %(assignment_name)s.')
             % {'task_name': assignment.name})
    body = _('When: %(date)s.\n\n'
             'Where:\n'
             'Project: %(project)s (Owner: %(cust)s).\n\n'
             '\033[1m New/Updated Assignment:\033[1m\n'
             'Name: %(assign)s.\n'
             'Requirements: %(req)s'
             ) % {'date': date.today(), 'project': assignment.project,
                  'cust': assignment.project.customer, 'assign': assignment,
                  'dev': assignment.dev, 'req': assignment.requirements}

    notif = Notification(name=title, description=body, int_type=1,
                         user=assignment.dev)
    return notif


def notif_negotiation(assignment):
    title = (_('Assignment: %(assignment_name)s. Event: %(event)s.')
             % {'task_name': assignment.name,
                'event': STATE[assignment.int_state-1]['next']})
    body = _('When: %(date)s.\n\n'
             'Where:\n'
             'Project: %(project)s (Owner: %(cust)s).\n'
             'Assignment: %(assign)s (Dev: %(dev)s).\n\n'
             '\033[1m Assignment change of state:\033[0m\n'
             'Event: %(event)s.\n'
             'New state: \'%(new_state)s\'. Waiting for: %(next_step)s.\n'
             'State description: %(state_desc)s\n'
             ) % {'date': date.today(), 'project': assignment.project,
                  'cust': assignment.project.customer, 'dev': assignment.dev,
                  'assign': assignment,
                  'new_state': STATE[assignment.int_state]['state'],
                  'event': STATE[assignment.int_state-1]['next'],
                  'next_step': STATE[assignment.int_state]['next'],
                  'state_desc': STATE[assignment.int_state]['desc']}

    if assignment.int_state in [-1, 2]:
        recipient = assignment.dev
        body = body + _(
            '\n'
            '\033[1m Comment about offer:\033[0m %(comment)s\n'
            ) % {'comment': assignment.deal_comment}
    if assignment.int_state in [-3, 4]:
        recipient = assignment.dev
    elif assignment.int_state in [1]:
        recipient = assignment.project.customer
        body = body + _(
            '\n'
            '\033[1m Offer:\033[0m\n'
            'Price: %(price)s €'
            'ETA: %(eta)s'
            ) % {'price': assignment.price,
                 'eta': assignment.eta}
    elif assignment.int_state in [-2, 3, 5]:
        recipient = assignment.project.customer

    notif = Notification(name=title, description=body, int_type=2,
                         user=recipient)
    return notif


def notif_closed_task(task):
    title = (_('New task: %(task_name)s.')
             % {'task_name': task.name})
    body = _('When: %(date)s.\n\n'
             'Where:\n'
             'Project: %(project)s.\n'
             'Assignment: %(assign)s (Dev: %(dev)s).\n\n'
             '\033[1m Closed task:\033[1m\n'
             'Name: %(task)s. Priority: %(priority)d.\n'
             ) % {'date': date.today(), 'project': task.assignment.project,
                  'assign': task.assignment, 'dev': task.assignment.dev,
                  'task': task, 'priority': task.priority}

    notif = Notification(name=title, description=body, int_type=3,
                         user=task.assignment.dev)
    return notif


def notif_comment_task(comment, recipient):
    title = (_('New comment in task: %(task_name)s.')
             % {'task_name': comment.task.name})
    body = _('When: %(date)s.\n\n'
             'Where:\n'
             'Project: %(project)s.\n'
             'Assignment: %(assign)s (Dev: %(dev)s).\n'
             'Task: %(task)s. Priority: %(priority)d.\n\n'
             '\033[1m Comment:\033[1m %(comment)s'
             ) % {'date': date.today(),
                  'project': comment.task.assignment.project,
                  'assign': comment.task.assignment,
                  'dev': comment.task.assignment.dev,
                  'task': comment.task, 'priority': comment.task.priority,
                  'comment': comment.comment}

    notif = Notification(name=title, description=body, int_type=4,
                         user=recipient)
    return notif


def notif_comment_assign(comment, recipient):
    title = (_('New comment in task: %(task_name)s.')
             % {'task_name': comment.assignment.name})
    body = _('When: %(date)s.\n\n'
             'Where:\n'
             'Project: %(project)s.\n'
             'Assignment: %(assign)s (Dev: %(dev)s).\n\n'
             '\033[1m Comment:\033[1m %(comment)s'
             ) % {'date': date.today(),
                  'project': comment.assignment.project,
                  'assign': comment.assignment,
                  'dev': comment.assignment.dev,
                  'comment': comment.comment}

    notif = Notification(name=title, description=body, int_type=5,
                         user=recipient)
    return notif
