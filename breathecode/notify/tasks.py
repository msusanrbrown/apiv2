import logging, os, requests, json
from celery import shared_task, Task
from django.core.serializers.json import DjangoJSONEncoder
from .actions import sync_slack_team_channel, sync_slack_team_users, send_email_message
from breathecode.services.slack.client import Slack
from breathecode.mentorship.models import MentorshipSession
from breathecode.authenticate.models import Token

API_URL = os.getenv('API_URL', '')

logger = logging.getLogger(__name__)


class BaseTaskWithRetry(Task):
    autoretry_for = (Exception, )
    #                                           seconds
    retry_kwargs = {'max_retries': 5, 'countdown': 60 * 5}
    retry_backoff = True


@shared_task
def async_slack_team_channel(team_id):
    logger.debug('Starting async_slack_team_channel')
    return sync_slack_team_channel(team_id)


@shared_task
def send_mentorship_starting_notification(session_id):
    logger.debug('Starting send_mentorship_starting_notification')

    session = MentorshipSession.objects.filter(id=session_id).first()

    token, created = Token.get_or_create(session.mentor.user, token_type='temporal', hours_length=2)

    send_email_message(
        'message', session.mentor.user.email, {
            'SUBJECT': 'Mentorship session starting',
            'MESSAGE':
            f'Mentee {session.mentee.first_name} {session.mentee.last_name} is joining your session, please come back to this email when the session is over to marke it as completed',
            'BUTTON': f'Finish and review this session',
            'LINK': f'{API_URL}/mentor/session/{session.id}?token={token.key}',
        })

    return True


@shared_task
def async_slack_team_users(team_id):
    logger.debug('Starting async_slack_team_users')
    return sync_slack_team_users(team_id)


@shared_task
def async_slack_action(post_data):
    logger.debug('Starting async_slack_action')
    try:
        client = Slack()
        success = client.execute_action(context=post_data)
        if success:
            logger.debug('Successfully process slack action')
            return True
        else:
            logger.error('Error processing slack action')
            return False

    except Exception as e:
        logger.exception('Error processing slack action')
        return False


@shared_task
def async_deliver_hook(target, payload, instance=None, hook_id=None, **kwargs):
    logger.debug('Starting async_deliver_hook')
    from .utils.hook_manager import HookManager
    """
    target:     the url to receive the payload.
    payload:    a python primitive data structure
    instance:   a possibly null "trigger" instance
    hook:       the defining Hook object (useful for removing)
    """
    response = requests.post(url=target,
                             data=json.dumps(payload, cls=DjangoJSONEncoder),
                             headers={'Content-Type': 'application/json'})

    if response.status_code == 410 and hook_id:
        HookModel = HookManager.get_hook_model()
        hook = HookModel.object.get(id=hook_id)
        hook.delete()

    # would be nice to log this, at least for a little while...
